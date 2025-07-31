import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.access_control import get_user_status
from file_tools.converter import txt_to_vcf, split_txt, vcf_to_txt, xls_to_vcf
from .menus import txt_menu, conversion_menu
from utils.logger import log_activity

# States for conversation
ASK_FILENAME, ASK_CONTACTNAME, ASK_CONTACTS_PER_FILE, ASK_START_ORDER, ASK_LINES_PER_FILE = range(5)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles file uploads and waits for user to choose an action."""
    user_id = update.effective_user.id
    log_activity(user_id, f"Uploaded file: {update.message.document.file_name}")
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("⚠️ Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    document = update.message.document
    file_name = document.file_name
    file = await document.get_file()

    # Store file data
    context.user_data['uploaded_file_name'] = file_name
    file_content = await file.download_as_bytearray()
    
    # Check if it's a TXT file for direct conversion
    if file_name.lower().endswith('.txt'):
        context.user_data['txt_content'] = file_content.decode('utf-8')
        
        # Show TXT to VCF conversion options
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = [
            [InlineKeyboardButton("📄 TXT ➝ VCF", callback_data='start_txt_vcf')],
            [InlineKeyboardButton("✂️ Split TXT", callback_data='start_split_txt')],
            [InlineKeyboardButton("🔙 Menu Utama", callback_data='back_to_main')]
        ]
        await update.message.reply_text(
            f"✅ File {file_name} diterima!\n\n"
            f"📊 Jumlah baris: {len(context.user_data['txt_content'].splitlines())}\n\n"
            f"Pilih aksi yang ingin dilakukan:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        context.user_data['uploaded_file_content'] = file_content
        await update.message.reply_text(f"File {file_name} diterima. Apa yang ingin Anda lakukan dengan file ini?", reply_markup=conversion_menu())

    return ConversationHandler.END

async def ask_filename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the base filename."""
    context.user_data['file_name_base'] = update.message.text
    await update.message.reply_text("📝 Masukkan nama kontak dasar:\n(Contoh: REXX)")
    return ASK_CONTACTNAME

async def ask_contactname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the base contact name."""
    context.user_data['contact_name_base'] = update.message.text
    await update.message.reply_text("🔢 Jumlah kontak per file?\n(Contoh: 50)")
    return ASK_CONTACTS_PER_FILE

async def ask_contacts_per_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the number of contacts per file."""
    try:
        contacts_per_file = int(update.message.text)
        if contacts_per_file <= 0:
            await update.message.reply_text("❌ Jumlah kontak harus lebih dari 0. Silakan coba lagi:")
            return ASK_CONTACTS_PER_FILE
        
        context.user_data['contacts_per_file'] = contacts_per_file
        await update.message.reply_text("🔢 Urutan awal file?\n(Contoh: 1)")
        return ASK_START_ORDER
    except ValueError:
        await update.message.reply_text("❌ Masukkan angka yang valid. Silakan coba lagi:")
        return ASK_CONTACTS_PER_FILE

async def ask_start_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the starting order and performs the conversion."""
    try:
        start_order = int(update.message.text)
        if start_order <= 0:
            await update.message.reply_text("❌ Urutan awal harus lebih dari 0. Silakan coba lagi:")
            return ASK_START_ORDER
        
        context.user_data['start_order'] = start_order

        # Get all data from user_data
        txt_content = context.user_data['txt_content']
        file_name_base = context.user_data['file_name_base']
        contact_name_base = context.user_data['contact_name_base']
        contacts_per_file = context.user_data['contacts_per_file']

        total_lines = len([line for line in txt_content.splitlines() if line.strip()])
        expected_files = (total_lines + contacts_per_file - 1) // contacts_per_file

        # Show summary before processing
        summary_text = f"""📋 RINGKASAN KONVERSI

📁 File dasar: {file_name_base}
👤 Kontak dasar: {contact_name_base}
🔢 Kontak per file: {contacts_per_file}
📊 Total nomor: {total_lines}
📦 File yang akan dibuat: {expected_files}

🎯 Format output:
• File: {file_name_base}-{start_order}.vcf, {file_name_base}-{start_order+1}.vcf, ...
• Kontak: {contact_name_base}-{start_order}-1, {contact_name_base}-{start_order}-2, ...

🔄 Memproses..."""

        await update.message.reply_text(summary_text)

        # Perform the conversion
        vcf_files = await asyncio.to_thread(txt_to_vcf, txt_content, file_name_base, contact_name_base, contacts_per_file, start_order)

        # Send completion message first
        await update.message.reply_text(f"✅ Konversi selesai! Mengirim {len(vcf_files)} file VCF...")

        # Send the files
        for i, vcf_file in enumerate(vcf_files, 1):
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=vcf_file['content'].encode('utf-8'),
                filename=vcf_file['name'],
                caption=f"📁 File {i}/{len(vcf_files)}: {vcf_file['name']}"
            )

        await update.message.reply_text("🎉 Semua file VCF berhasil dikirim!\n\nTerima kasih telah menggunakan TUTOR KIKS Bot!")

        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("❌ Masukkan angka yang valid. Silakan coba lagi:")
        return ASK_START_ORDER

async def ask_lines_per_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the number of lines per file and performs the split."""
    lines_per_file = int(update.message.text)
    txt_content = context.user_data['txt_content']

    await update.message.reply_text("Memproses file Anda...")
    split_files = await asyncio.to_thread(split_txt, txt_content, lines_per_file)

    for split_file in split_files:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=split_file['content'].encode('utf-8'),
            filename=split_file['name']
        )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Konversi dibatalkan.")
    return ConversationHandler.END
