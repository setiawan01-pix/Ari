from apscheduler.schedulers.background import BackgroundScheduler
from file_tools.converter import txt_to_vcf # Example import
from telegram import Bot
from config import TOKEN
import asyncio

scheduler = BackgroundScheduler()

def scheduled_conversion(chat_id, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    """The job to be executed at the scheduled time."""
    async def send_files():
        bot = Bot(TOKEN)
        vcf_files = txt_to_vcf(file_content, file_name_base, contact_name_base, contacts_per_file, start_order)
        for vcf_file in vcf_files:
            await bot.send_document(
                chat_id=chat_id,
                document=vcf_file['content'].encode('utf-8'),
                filename=vcf_file['name']
            )
    
    # Run the async function in a new event loop
    asyncio.run(send_files())

def add_scheduled_job(chat_id, run_date, file_content, file_name_base, contact_name_base, contacts_per_file, start_order):
    """Adds a job to the scheduler."""
    scheduler.add_job(
        scheduled_conversion,
        'date',
        run_date=run_date,
        args=[chat_id, file_content, file_name_base, contact_name_base, contacts_per_file, start_order]
    )
