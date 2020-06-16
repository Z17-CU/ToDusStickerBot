import glob
import json

from downloader import Downloader
from storage import Storage


class Processor:

    def __init__(self, s3_client):
        self.s3_client = s3_client
        self.s3_client.download_index("/tmp/index.json")
        with open('/tmp/index.json', 'r') as f:
            self.stickers_index = json.load(f)

    def filter(self, update, context):
        if not hasattr(update.message, 'sticker'):
            return

        if self.s3_client.sticker_exists(update.message.sticker.set_name):
            update.message.reply_text("Este pack ya existe en todus! " + update.message.sticker.set_name)
            return

        update.message.reply_text("Procesando " + update.message.sticker.set_name)

        downloader = Downloader(context.bot)
        sticker_dict = downloader.download(update.message.sticker.set_name)

        for file_path in glob.iglob(sticker_dict['name'] + '/**/*.tgs', recursive=True):
            self.s3_client.upload_file(file_path, file_path)

        storage = Storage()
        storage.zip_dir(sticker_dict['name'], sticker_dict['name']+'.zip')

        self.s3_client.upload_file(sticker_dict['name']+'.zip', sticker_dict['name']+"/pack.zip")
