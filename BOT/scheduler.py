from apscheduler.schedulers.asyncio import AsyncIOScheduler
from BOT.file_tools.converter import txt_to_vcf # Example import
from telegram import Bot
from BOT.config import TOKEN

scheduler = AsyncIOScheduler()

async def scheduled_conversion(chat_id, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    """The job to be executed at the scheduled time."""
    bot = Bot(TOKEN)
    vcf_files = txt_to_vcf(file_content, file_name_base, contact_name_base, contacts_per_file, start_order)
    for vcf_file in vcf_files:
        await bot.send_document(
            chat_id=chat_id,
            document=vcf_file['content'].encode('utf-8'),
            filename=vcf_file['name']
        )

def add_scheduled_job(chat_id, run_date, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    """Adds a job to the scheduler."""
    scheduler.add_job(
        scheduled_conversion,
        'date',
        run_date=run_date,
        args=[chat_id, file_content, file_name_base, contact_name_base, contacts_per_file, start_order]
    )
