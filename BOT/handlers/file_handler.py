import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.access_control import get_user_status
from file_tools.converter import txt_to_vcf, split_txt, vcf_to_txt, xls_to_vcf
from .menus import txt_menu
from utils.logger import log_activity

# States for conversation
ASK_FILENAME, ASK_CONTACTNAME, ASK_CONTACTS_PER_FILE, ASK_START_ORDER, ASK_LINES_PER_FILE = range(5)

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles file uploads and waits for user to choose an action."""
    user_id = update.effective_user.id
    log_activity(user_id, f"Uploaded file: {update.message.document.file_name}")
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    document = update.message.document
    file_name = document.file_name
    file = await document.get_file()

    context.user_data['uploaded_file_name'] = file_name
    context.user_data['uploaded_file_content'] = await file.download_as_bytearray()

    await update.message.reply_text(f"File {file_name} diterima. Apa yang ingin Anda lakukan dengan file ini?", reply_markup=conversion_menu())

    return ConversationHandler.END

async def ask_filename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the base filename."""
    context.user_data['file_name_base'] = update.message.text
    await update.message.reply_text("Masukkan nama kontak dasar:")
    return ASK_CONTACTNAME

async def ask_contactname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the base contact name."""
    context.user_data['contact_name_base'] = update.message.text
    await update.message.reply_text("Jumlah kontak per file?")
    return ASK_CONTACTS_PER_FILE

async def ask_contacts_per_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the number of contacts per file."""
    context.user_data['contacts_per_file'] = int(update.message.text)
    await update.message.reply_text("Urutan awal file?")
    return ASK_START_ORDER

async def ask_start_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the starting order and performs the conversion."""
    context.user_data['start_order'] = int(update.message.text)

    # Get all data from user_data
    txt_content = context.user_data['txt_content']
    file_name_base = context.user_data['file_name_base']
    contact_name_base = context.user_data['contact_name_base']
    contacts_per_file = context.user_data['contacts_per_file']
    start_order = context.user_data['start_order']

    # Perform the conversion
    await update.message.reply_text("Memproses file Anda...")
    vcf_files = await asyncio.to_thread(txt_to_vcf, txt_content, file_name_base, contact_name_base, contacts_per_file, start_order)

    # Send the files
    for vcf_file in vcf_files:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=vcf_file['content'].encode('utf-8'),
            filename=vcf_file['name']
        )

    return ConversationHandler.END

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
