from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import os
from os.path import basename
from pathlib import Path
from dotenv import load_dotenv
import glob, json

from minio import Minio
from minio.error import ResponseError


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

minioClient = Minio(os.environ.get('s3_url'),
                    access_key=os.environ.get('s3_access_key'),
                    secret_key=os.environ.get('s3_secret_key'),
                    secure=True)

stickerBucket = os.environ.get('s3_bucket')
stickerList = "list.json"

def updateList(stickerJson):
    print(stickerJson)


def saveToS3(stickerJson):

    if not minioClient.bucket_exists(stickerBucket):
        minioClient.make_bucket(stickerBucket)
    for filepath in glob.iglob(stickerJson['name']+'/**/*.tgs', recursive=True):
        print(filepath)
        minioClient.fput_object(stickerBucket, filepath, filepath)

    updateList(stickerJson)


def processDownload(sticker, update, context):
    stickerSet = context.bot.getStickerSet(sticker.set_name)
    stickerJson = {'name': stickerSet.name, 'title': stickerSet.title, 'stickers':[]}

    if not os.path.exists(stickerSet.name):
        os.makedirs(stickerSet.name + "/thumb")

    file = context.bot.getFile(stickerSet.thumb.file_id)
    file.download(stickerSet.name + "/thumb/" + basename(file.file_path))
    stickerJson['thumb'] = stickerSet.name + "/thumb/" + basename(file.file_path)
    for st in stickerSet.stickers:
        file = context.bot.getFile(st.file_id)
        file.download(stickerSet.name + "/" + basename(file.file_path))
        stickerJson['stickers'].append(stickerSet.name + "/" + basename(file.file_path))

    saveToS3(stickerJson)

    update.message.reply_text("Añadido " + stickerSet.name)


def sticker(update, context):
    if hasattr(update.message, 'sticker'):
        processDownload(update.message.sticker, update, context)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get('bot_key'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.sticker, sticker))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
