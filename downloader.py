import os
from os.path import basename


class Downloader:

    def __init__(self, bot):
        self.bot = bot

    def download(self, sticker_name):
        sticker_set = self.bot.getStickerSet(sticker_name)
        sticker_json = {'name': sticker_set.name, 'title': sticker_set.title, 'stickers': []}

        if not os.path.exists(sticker_set.name):
            os.makedirs(sticker_set.name + "/thumb")

        file = self.bot.getFile(sticker_set.thumb.file_id)
        file.download(sticker_set.name + "/thumb/" + basename(file.file_path))
        sticker_json['thumb'] = sticker_set.name + "/thumb/" + basename(file.file_path)
        for st in sticker_set.stickers:
            file = self.bot.getFile(st.file_id)
            file.download(sticker_set.name + "/" + basename(file.file_path))
            sticker_json['stickers'].append(sticker_set.name + "/" + basename(file.file_path))

        return sticker_json
