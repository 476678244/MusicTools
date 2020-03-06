from os import listdir
from os.path import isfile, join

my_path = '/Volumes/WD1024G/Music/cdbao/100'
found_albums = list()
for f in listdir(my_path):
    if (not isfile(join(my_path, f)) and not f.startswith('.')):
        dir = join(my_path, f)
        print(dir)
        for album in listdir(dir):
            if (not album.startswith('.')):
                found_albums.append((join(dir, album), album))

dest_dir = '/Volumes/WD1024G/Music/cdbao_union'
test_album = found_albums[0]
# import shutil
#
# shutil.copytree(test_album[0], join(dest_dir, test_album[1]))

import tools.cp_with_prog as cp_with_prog
import os

for found_album in found_albums:
    print(found_album)
    os.mkdir(join(dest_dir, found_album))
    for file in listdir(found_album[0]):
        print(file)
        cp_with_prog.copy(
            join(found_album[0], file),
            join(join(dest_dir, found_album[1]), file),
            cp_with_prog.progress
        )
