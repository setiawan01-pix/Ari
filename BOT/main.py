import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from config import TOKEN, ADMIN_ID
from handlers.menus import main_menu
from handlers.callback_handler import button
from admin_access.admin_features import activate_premium
from handlers.file_handler import (
    handle_file,
    ask_filename,
    ask_contactname,
    ask_contacts_per_file,
    ask_start_order,
    ask_lines_per_file,
    cancel,
    ASK_FILENAME,
    ASK_CONTACTNAME,
    ASK_CONTACTS_PER_FILE,
    ASK_START_ORDER,
    ASK_LINES_PER_FILE,
)
from handlers.file_tools_handler import (
    handle_merge,
    waiting_files,
    ask_merge_filename,
    perform_merge,
    cancel as cancel_merge,
    ASK_MERGE_FILENAME,
    handle_check_duplicates,
    handle_remove_duplicates,
    handle_add_contact,
    waiting_file_for_contact,
    ask_contact_name,
    perform_add_contact,
    cancel as cancel_add_contact,
    ASK_CONTACT_NAME,
    ASK_CONTACT_PHONE,
    handle_rename_file,
    waiting_file_for_rename,
    perform_rename,
    cancel as cancel_rename,
    ASK_NEW_FILENAME,
    handle_delete_number,
    waiting_file_for_delete,
    perform_delete_number,
    cancel as cancel_delete,
    ASK_NUMBER_TO_DELETE,
    handle_split_file,
    waiting_file_for_split,
    perform_split_file,
    cancel as cancel_split,
    ASK_CONTACTS_PER_SPLIT_FILE,
    handle_manual_input,
    ask_manual_input_name,
    ask_manual_input_phone,
    ask_file_type,
    perform_manual_input_save,
    cancel as cancel_manual_input,
    ASK_MANUAL_INPUT_NAME,
    ASK_MANUAL_INPUT_PHONE,
    ASK_FILE_TYPE,
)
from admin_access.admin_features import (
    broadcast_message, set_payment_method, set_qr_code, set_price,
    schedule_conversion_job, get_user_list, kick_user, set_welcome_message
)
from functools import wraps

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def admin_only(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            await update.message.reply_text("Anda tidak memiliki izin untuk menggunakan perintah ini.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

from BOT.utils.caching import get_customization_data
from BOT.utils.logger import log_activity

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a menu when the command /start is issued."""
    log_activity(update.effective_user.id, "/start")
    custom_data = get_customization_data()
    welcome_message = custom_data.get("welcome_message", "Selamat datang! Silakan pilih opsi:")
    await update.message.reply_text(welcome_message, reply_markup=main_menu())

@admin_only
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the broadcast conversation."""
    await update.message.reply_text("Masukkan pesan yang ingin Anda siarkan:")
    return 'BROADCAST_MESSAGE'

async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends the broadcast message."""
    message = update.message.text
    await broadcast_message(context, message)
    await update.message.reply_text("Pesan siaran telah dikirim.")
    return ConversationHandler.END

@admin_only
async def setpayment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the payment method."""
    try:
        method = " ".join(context.args)
        set_payment_method(method)
        await update.message.reply_text(f"Metode pembayaran telah diubah menjadi: {method}")
    except IndexError:
        await update.message.reply_text("Penggunaan: /setpayment <metode>")

@admin_only
async def setqr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the QR code URL."""
    try:
        url = context.args[0]
        set_qr_code(url)
        await update.message.reply_text(f"URL kode QR telah diubah.")
    except IndexError:
        await update.message.reply_text("Penggunaan: /setqr <url>")

@admin_only
async def setprice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the price for a duration."""
    try:
        duration = context.args[0]
        price = int(context.args[1])
        set_price(duration, price)
        await update.message.reply_text(f"Harga untuk {duration} hari telah diubah menjadi: {price}")
    except (IndexError, ValueError):
        await update.message.reply_text("Penggunaan: /setprice <durasi> <harga>")


@admin_only
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Schedules a conversion job."""
    try:
        args = context.args
        run_date_str = f"{args[0]} {args[1]}"
        file_id = args[2]
        file_name_base = args[3]
        contact_name_base = args[4]
        contacts_per_file = int(args[5])
        start_order = int(args[6])

        file = await context.bot.get_file(file_id)
        file_content = (await file.download_as_bytearray()).decode('utf-8')

        if schedule_conversion_job(update.effective_chat.id, run_date_str, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
            await update.message.reply_text("Konversi telah dijadwalkan.")
        else:
            await update.message.reply_text("Format tanggal tidak valid. Gunakan YYYY-MM-DD HH:MM:SS")

    except (IndexError, ValueError):
        await update.message.reply_text("Penggunaan: /schedule <YYYY-MM-DD> <HH:MM:SS> <file_id> <nama_file_dasar> <nama_kontak_dasar> <kontak_per_file> <urutan_awal>")

@admin_only
async def listusers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all users."""
    user_list = get_user_list()
    await update.message.reply_text(user_list)

@admin_only
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Kicks a user."""
    try:
        user_id = context.args[0]
        if kick_user(user_id):
            await update.message.reply_text(f"Pengguna {user_id} telah dihapus.")
        else:
            await update.message.reply_text(f"Pengguna {user_id} tidak ditemukan.")
    except IndexError:
        await update.message.reply_text("Penggunaan: /kick <user_id>")

@admin_only
async def ubahsambutan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets the welcome message."""
    try:
        message = " ".join(context.args)
        set_welcome_message(message)
        await update.message.reply_text("Pesan sambutan telah diubah.")
    except IndexError:
        await update.message.reply_text("Penggunaan: /ubahsambutan <pesan>")

@admin_only
async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Activates premium for a user."""
    try:
        user_id = context.args[0]
        days = int(context.args[1])
        if activate_premium(user_id, days):
            await update.message.reply_text(f"Pengguna {user_id} telah diaktifkan premium selama {days} hari.")
        else:
            await update.message.reply_text(f"Gagal mengaktifkan premium untuk pengguna {user_id}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Penggunaan: /adduser <user_id> <jumlah_hari>")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).concurrent_updates(True).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            ASK_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_filename)],
            ASK_CONTACTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contactname)],
            ASK_CONTACTS_PER_FILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contacts_per_file)],
            ASK_START_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_start_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        map_to_parent={
            # End the conversation when returning ConversationHandler.END
            ConversationHandler.END: ConversationHandler.END,
        }
    )

    split_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^split_txt$')],
        states={
            ASK_LINES_PER_FILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_lines_per_file)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


    merge_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("merge", handle_merge)],
        states={
            'WAITING_FILES': [MessageHandler(filters.Document.ALL, waiting_files)],
            ASK_MERGE_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_merge)],
        },
        fallbacks=[CommandHandler("done", ask_merge_filename), CommandHandler("cancel", cancel_merge)],
    )

    application.add_handler(conv_handler)
    application.add_handler(split_conv_handler)
    add_contact_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^add_contact$')],
        states={
            'WAITING_FILE_FOR_CONTACT': [MessageHandler(filters.Document.ALL, waiting_file_for_contact)],
            ASK_CONTACT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_contact_name)],
            ASK_CONTACT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_add_contact)],
        },
        fallbacks=[CommandHandler("cancel", cancel_add_contact)],
    )

    rename_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^rename_file$')],
        states={
            'WAITING_FILE_FOR_RENAME': [MessageHandler(filters.Document.ALL, waiting_file_for_rename)],
            ASK_NEW_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_rename)],
        },
        fallbacks=[CommandHandler("cancel", cancel_rename)],
    )

    application.add_handler(merge_conv_handler)
    delete_number_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^delete_number$')],
        states={
            'WAITING_FILE_FOR_DELETE': [MessageHandler(filters.Document.ALL, waiting_file_for_delete)],
            ASK_NUMBER_TO_DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_delete_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel_delete)],
    )

    application.add_handler(add_contact_conv_handler)
    split_file_tool_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^split_file_tool$')],
        states={
            'WAITING_FILE_FOR_SPLIT': [MessageHandler(filters.Document.ALL, waiting_file_for_split)],
            ASK_CONTACTS_PER_SPLIT_FILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, perform_split_file)],
        },
        fallbacks=[CommandHandler("cancel", cancel_split)],
    )

    manual_input_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^manual_input$')],
        states={
            ASK_MANUAL_INPUT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_manual_input_name)],
            ASK_MANUAL_INPUT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_manual_input_phone)],
            ASK_FILE_TYPE: [CallbackQueryHandler(perform_manual_input_save)],
        },
        fallbacks=[CommandHandler("done", ask_file_type), CommandHandler("cancel", cancel_manual_input)],
    )

    application.add_handler(rename_conv_handler)
    application.add_handler(delete_number_conv_handler)
    file_info_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern='^file_info$')],
        states={
            WAITING_FILE_FOR_INFO: [MessageHandler(filters.Document.ALL, perform_get_file_info)],
        },
        fallbacks=[CommandHandler("cancel", cancel_file_info)],
    )

    application.add_handler(split_file_tool_conv_handler)
    broadcast_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast)],
        states={
            'BROADCAST_MESSAGE': [MessageHandler(filters.TEXT & ~filters.COMMAND, send_broadcast)],
        },
        fallbacks=[CommandHandler("cancel", cancel)], # A generic cancel handler can be used here
    )

    application.add_handler(manual_input_conv_handler)
    application.add_handler(file_info_conv_handler)
    application.add_handler(broadcast_conv_handler)
    application.add_handler(MessageHandler(filters.Document.ALL & filters.CaptionRegex(r'/checkduplicates'), handle_check_duplicates))
    application.add_handler(CallbackQueryHandler(handle_remove_duplicates, pattern='^remove_duplicates$'))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("adduser", adduser))
    application.add_handler(CommandHandler("setpayment", setpayment))
    application.add_handler(CommandHandler("setqr", setqr))
    application.add_handler(CommandHandler("setprice", setprice))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler("listusers", listusers))
    application.add_handler(CommandHandler("kick", kick))
    application.add_handler(CommandHandler("ubahsambutan", ubahsambutan))
    application.add_handler(CallbackQueryHandler(button))

    from BOT.scheduler import scheduler
    scheduler.start()
    application.run_polling()

if __name__ == "__main__":
    main()
