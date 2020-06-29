import glob
import shutil,os

from downloader import Downloader
from storage import Storage


class Processor:

    def __init__(self, s3_client, pg_client):
        self.s3_client = s3_client
        self.pg_client = pg_client

    def filter(self, update, context):
        if not hasattr(update.message, 'sticker'):
            return

        if not update.message.sticker.is_animated:
            update.message.reply_text("Este pack no es compatible " + update.message.sticker.set_name)
            return

        if self.s3_client.sticker_exists(update.message.sticker.set_name):
            update.message.reply_text("Este pack ya existe en toDus! " + update.message.sticker.set_name)
            return

        update.message.reply_text("Procesando " + update.message.sticker.set_name)

        downloader = Downloader(context.bot)
        sticker_dict = downloader.download(update.message.sticker.set_name)

        for file_path in glob.iglob(sticker_dict['name'] + '/**/*.tgs', recursive=True):
            self.s3_client.upload_file(file_path, file_path)

        storage = Storage()
        storage.zip_dir(sticker_dict['name'], sticker_dict['name']+'.zip')

        self.s3_client.upload_file(sticker_dict['name']+'.zip', sticker_dict['name']+"/pack.zip")
        shutil.rmtree(sticker_dict['name'], True)
        os.remove(sticker_dict['name']+'.zip')
        self.pg_client.insert_sticker_pack(sticker_dict['name'], sticker_dict['title'], sticker_dict['thumb'])

        update.message.reply_text("Añadido " + update.message.sticker.set_name)
