import os
from os.path import basename
from zipfile import ZipFile


class Storage:

    # Zip the files from given directory that matches the filter
    def zip_dir(self, dir_name, zip_file):
        # create a ZipFile object
        with ZipFile(zip_file, 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, _, files_names in os.walk(dir_name):
                for filename in files_names:
                    if 'tgs' in filename:
                        # create complete file_path of file in directory
                        file_path = os.path.join(folderName, filename)
                        # Add file to zip
                        zipObj.write(file_path)
