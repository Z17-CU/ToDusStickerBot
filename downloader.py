import os
from os.path import basename, splitext


class Downloader:

    def __init__(self, bot):
        self.bot = bot

    def download(self, sticker_name):
        sticker_set = self.bot.getStickerSet(sticker_name)
        sticker_json = {'name': sticker_set.name, 'title': sticker_set.title, 'stickers': [],
                        'animated': sticker_set.is_animated}

        if not os.path.exists(sticker_set.name):
            os.makedirs(sticker_set.name + "/thumb")

        have_thumb = False
        if sticker_set.thumb is not None:
            have_thumb = True
            file = self.bot.getFile(sticker_set.thumb.file_id)
            filename, extension = splitext(basename(file.file_path))
            file.download(sticker_set.name + "/thumb/thumb" + extension)
            sticker_json['thumb'] = sticker_set.name + "/thumb/thumb" + extension
        for index, st in enumerate(sticker_set.stickers, start=1):
            file = self.bot.getFile(st.file_id)
            filename, extension = splitext(basename(file.file_path))
            filename = str(index) + extension
            if not have_thumb:
                sticker_json['thumb'] = sticker_set.name + "/" + filename
            file.download(sticker_set.name + "/" + filename)
            sticker_json['stickers'].append(sticker_set.name + "/" + filename)

        return sticker_json
