import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from utils.access_control import get_user_status
from file_tools.manipulator import merge_files, check_duplicates, remove_duplicates, add_contact, delete_number, split_file, create_file_from_manual_input

# States for conversation
ASK_MERGE_FILENAME, ASK_CONTACT_NAME, ASK_CONTACT_PHONE, ASK_NEW_FILENAME, ASK_NUMBER_TO_DELETE, ASK_CONTACTS_PER_SPLIT_FILE, ASK_MANUAL_INPUT_NAME, ASK_MANUAL_INPUT_PHONE, ASK_FILE_TYPE, WAITING_FILE_FOR_INFO = range(10)

async def handle_merge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the merge process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    await update.message.reply_text("Silakan kirim file yang ingin Anda gabungkan. Kirim /done jika sudah selesai.")
    context.user_data['merge_files'] = []
    return 'WAITING_FILES'

async def waiting_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Waits for files to merge."""
    document = update.message.document
    file = await document.get_file()
    file_content = (await file.download_as_bytearray()).decode('utf-8')
    context.user_data['merge_files'].append(file_content)
    return 'WAITING_FILES'

async def ask_merge_filename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the merged filename."""
    await update.message.reply_text("Gunakan nama file hasil apa?")
    return ASK_MERGE_FILENAME

async def perform_merge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the merge and sends the file."""
    output_filename = update.message.text
    await update.message.reply_text("Menggabungkan file...")
    merged_content = await asyncio.to_thread(merge_files, context.user_data['merge_files'])

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=merged_content.encode('utf-8'),
        filename=output_filename
    )

    return ConversationHandler.END

async def handle_check_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the check duplicates feature."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return

    document = update.message.document
    file = await document.get_file()
    content = (await file.download_as_bytearray()).decode('utf-8')
    context.user_data['file_content'] = content

    await update.message.reply_text("Mengecek duplikat...")
    total, unique, duplicates = await asyncio.to_thread(check_duplicates, content)

    keyboard = [[InlineKeyboardButton("Hapus duplikat & kirim ulang", callback_data='remove_duplicates')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ {total} total | {unique} unik | ❗ {duplicates} duplikat",
        reply_markup=reply_markup
    )

async def handle_remove_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the remove duplicates callback."""
    query = update.callback_query
    await query.answer()

    content = context.user_data['file_content']
    await query.edit_message_text("Menghapus duplikat...")
    cleaned_content = await asyncio.to_thread(remove_duplicates, content)

    await context.bot.send_document(
        chat_id=query.message.chat_id,
        document=cleaned_content.encode('utf-8'),
        filename="cleaned.txt"
    )

async def handle_add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the add contact process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    await update.message.reply_text("Silakan kirim file .txt atau .vcf yang ingin Anda tambahkan kontaknya.")
    return 'WAITING_FILE_FOR_CONTACT'

async def waiting_file_for_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Waits for the file to add a contact to."""
    document = update.message.document
    context.user_data['is_vcf'] = document.file_name.endswith(".vcf")
    file = await document.get_file()
    context.user_data['file_content'] = (await file.download_as_bytearray()).decode('utf-8')
    await update.message.reply_text("Masukkan nama kontak baru:")
    return ASK_CONTACT_NAME

async def ask_contact_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the new contact's name."""
    context.user_data['contact_name'] = update.message.text
    await update.message.reply_text("Masukkan nomor telepon baru:")
    return ASK_CONTACT_PHONE

async def perform_add_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the add contact and sends the file."""
    phone = update.message.text
    content = context.user_data['file_content']
    name = context.user_data['contact_name']
    is_vcf = context.user_data['is_vcf']

    await update.message.reply_text("Menambahkan kontak...")
    updated_content = await asyncio.to_thread(add_contact, content, name, phone, is_vcf)

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=updated_content.encode('utf-8'),
        filename="updated_file"
    )

    return ConversationHandler.END

async def handle_rename_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the rename file process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    await update.message.reply_text("Silakan kirim file yang ingin Anda ganti namanya.")
    return 'WAITING_FILE_FOR_RENAME'

async def waiting_file_for_rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Waits for the file to rename."""
    document = update.message.document
    context.user_data['file_to_rename'] = document
    await update.message.reply_text("Masukkan nama baru:")
    return ASK_NEW_FILENAME

async def perform_rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the rename and sends the file."""
    new_name = update.message.text
    document = context.user_data['file_to_rename']
    file = await document.get_file()

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=file.file_id,
        filename=new_name
    )

    return ConversationHandler.END

async def handle_delete_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the delete number process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    await update.message.reply_text("Silakan kirim file .txt atau .vcf yang ingin Anda hapus nomornya.")
    return 'WAITING_FILE_FOR_DELETE'

async def waiting_file_for_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Waits for the file to delete a number from."""
    document = update.message.document
    context.user_data['is_vcf'] = document.file_name.endswith(".vcf")
    file = await document.get_file()
    context.user_data['file_content'] = (await file.download_as_bytearray()).decode('utf-8')
    await update.message.reply_text("Masukkan nomor yang ingin dihapus:")
    return ASK_NUMBER_TO_DELETE

async def perform_delete_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the delete number and sends the file."""
    number = update.message.text
    content = context.user_data['file_content']
    is_vcf = context.user_data['is_vcf']

    await update.message.reply_text("Menghapus nomor...")
    updated_content = await asyncio.to_thread(delete_number, content, number, is_vcf)

    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document=updated_content.encode('utf-8'),
        filename="updated_file"
    )

    return ConversationHandler.END

async def handle_split_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the split file process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    await update.message.reply_text("Silakan kirim file yang ingin Anda pecah.")
    return 'WAITING_FILE_FOR_SPLIT'

async def waiting_file_for_split(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Waits for the file to split."""
    document = update.message.document
    context.user_data['is_vcf'] = document.file_name.endswith(".vcf")
    file = await document.get_file()
    context.user_data['file_content'] = (await file.download_as_bytearray()).decode('utf-8')
    await update.message.reply_text("Jumlah kontak per bagian?")
    return ASK_CONTACTS_PER_SPLIT_FILE

async def perform_split_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the split and sends the files."""
    contacts_per_file = int(update.message.text)
    content = context.user_data['file_content']
    is_vcf = context.user_data['is_vcf']

    await update.message.reply_text("Memecah file...")
    split_files = await asyncio.to_thread(split_file, content, contacts_per_file, is_vcf)

    for f in split_files:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=f['content'].encode('utf-8'),
            filename=f['name']
        )

    return ConversationHandler.END

async def handle_manual_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the start of the manual input process."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)

    if status not in ["trial", "premium"]:
        await update.message.reply_text("Akses Anda telah berakhir. Silakan perpanjang langganan Anda.")
        return ConversationHandler.END

    context.user_data['manual_contacts'] = []
    await update.message.reply_text("Masukkan nama kontak (atau /done untuk selesai):")
    return ASK_MANUAL_INPUT_NAME

async def ask_manual_input_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the contact's name for manual input."""
    context.user_data['current_contact_name'] = update.message.text
    await update.message.reply_text("Masukkan nomor telepon:")
    return ASK_MANUAL_INPUT_PHONE

async def ask_manual_input_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the contact's phone for manual input."""
    phone = update.message.text
    name = context.user_data['current_contact_name']
    context.user_data['manual_contacts'].append({"name": name, "phone": phone})
    await update.message.reply_text("Masukkan nama kontak (atau /done untuk selesai):")
    return ASK_MANUAL_INPUT_NAME

async def ask_file_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the file type to save as."""
    keyboard = [[InlineKeyboardButton("TXT", callback_data='save_as_txt')],
                [InlineKeyboardButton("VCF", callback_data='save_as_vcf')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Simpan sebagai:", reply_markup=reply_markup)
    return ASK_FILE_TYPE

async def perform_manual_input_save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Performs the save for manual input."""
    query = update.callback_query
    await query.answer()

    as_vcf = query.data == 'save_as_vcf'
    contacts = context.user_data['manual_contacts']

    await query.edit_message_text("Membuat file...")
    content = await asyncio.to_thread(create_file_from_manual_input, contacts, as_vcf)

    filename = "manual_input.vcf" if as_vcf else "manual_input.txt"

    await context.bot.send_document(
        chat_id=query.message.chat_id,
        document=content.encode('utf-8'),
        filename=filename
    )

    return ConversationHandler.END


async def perform_get_file_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets information about the uploaded file."""
    user_id = update.effective_user.id
    status = get_user_status(user_id)
    
    if status not in ["trial", "premium"]:
        await update.message.reply_text("❌ Anda harus memiliki akses trial atau premium untuk menggunakan fitur ini.")
        return ConversationHandler.END
    
    document = update.message.document
    if document:
        file_name = document.file_name
        file_size = document.file_size
        
        # Convert file size to readable format
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        
        file_info = f"📁 **Informasi File:**\n\n"
        file_info += f"📝 Nama: {file_name}\n"
        file_info += f"📊 Ukuran: {size_str}\n"
        file_info += f"🔗 ID File: {document.file_id}"
        
        await update.message.reply_text(file_info, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Tidak ada file yang ditemukan.")
    
    return ConversationHandler.END

async def cancel_file_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the file info operation."""
    await update.message.reply_text("Operasi informasi file dibatalkan.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("Operasi dibatalkan.")
    return ConversationHandler.END
