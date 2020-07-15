import os
from os.path import basename, splitext


class Downloader:

    def __init__(self, bot):
        self.bot = bot

    def download(self, sticker_name):
        sticker_set = self.bot.getStickerSet(sticker_name)
        sticker_json = {'name': sticker_set.name, 'title': sticker_set.title, 'stickers': [], 'animated':sticker_set.is_animated}

        if not os.path.exists(sticker_set.name):
            os.makedirs(sticker_set.name + "/thumb")

        have_thumb = False
        if sticker_set.thumb is not None:
            have_thumb = True
            file = self.bot.getFile(sticker_set.thumb.file_id)
            file.download(sticker_set.name + "/thumb/" + basename(file.file_path))
            sticker_json['thumb'] = sticker_set.name + "/thumb/" + basename(file.file_path)
        for st in sticker_set.stickers:
            file = self.bot.getFile(st.file_id)
            if not have_thumb:
                sticker_json['thumb'] = sticker_set.name + "/" + basename(file.file_path)
            file.download(sticker_set.name + "/" + basename(file.file_path))
            sticker_json['stickers'].append(sticker_set.name + "/" + basename(file.file_path))

        return sticker_json
