from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv

from downloader import Downloader
from processor import Processor
from s3_client import S3Client
from pg_client import PgClient

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()


def main():
    s3_client = S3Client(os.environ.get('s3_url'),
                         os.environ.get('s3_access_key'),
                         os.environ.get('s3_secret_key'),
                         os.environ.get('s3_bucket'),
                         )

    pg_client = PgClient(
        host=os.environ.get('pg_host'),
        port=os.environ.get('pg_port'),
        user=os.environ.get('pg_user'),
        passwd=os.environ.get('pg_pass'),
        db=os.environ.get('pg_db')
    )
    processor = Processor(s3_client, pg_client)

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get('bot_key'), use_context=True, )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.sticker, processor.filter))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
