from os import listdir
from os.path import isfile, join

import tools.cp_with_prog as cp_with_prog
import os


# test_album = found_albums[0]
# import shutil
# shutil.copytree(test_album[0], join(dest_dir, test_album[1]))

def find_albums(input_path: str):
    result = list()
    for f in listdir(input_path):
        if not isfile(join(input_path, f)) and not f.startswith('.'):
            dir_path = join(input_path, f)
            print(dir_path)
            for album in listdir(dir_path):
                if not album.startswith('.'):
                    result.append((join(dir_path, album), album))
    return result


def copy_to_union(union_dir: str, albums: list):
    for album in albums:
        os.mkdir(join(union_dir, album[1]))
        for file in listdir(album[0]):
            print('Album: %s, File: %s' % (album, file))
            print("Total Progress: %s "% "{0:.0%}".format(albums.index(album) / len(albums)))
            cp_with_prog.copy(
                join(album[0], file),
                join(join(union_dir, album[1]), file),
                cp_with_prog.progress
            )


copy_to_union(
    '/Volumes/Backups.backupdb/Music/cdbao_union',
    find_albums('/Volumes/WD1024G/Music/cdbao/100')
)

copy_to_union(
    '/Volumes/Backups.backupdb/Music/cdbao_union',
    find_albums('/Volumes/WD1024G/Music/cdbao/200')
)
