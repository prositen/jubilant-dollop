import os
import re
import shutil

from collections import defaultdict

""" 
Scans through a collection of files named according to FILE_REGEXP to find duplicates.

When more than one occurrence of a title is found, keep one according to heuristics in `region_sort` and
move the others to BACKUP_PATH

"""
__author__ = 'Anna Holmgren'

COLLECTION_PATH = r""
BACKUP_PATH = r""
FILE_REGEXP = re.compile(r"\d+ - ([^)]*) (\([^)]*\)).*\.\w+")


class FileInfo(object):
    def __init__(self, title, region, file_name, path):
        self.title = title
        self.file_name = file_name
        self.region = region
        self.path = path

    def __str__(self):
        return os.path.join(self.path, self.file_name)


def region_sort(file_info):
    region = file_info.region[1]
    if region == 'E':
        return 0
    elif region == 'U':
        return 1
    elif region == 'J':
        return 2
    else:
        return 3


def main():
    move_duplicates(find_duplicates(find_files(COLLECTION_PATH)))


def move_duplicates(files):
    for dupe in files:
        print("Moving {} to {}".format(dupe, BACKUP_PATH))
        shutil.move(dupe, BACKUP_PATH)
    if len(files) == 0:
        print("No duplicate files found")


def find_duplicates(files):
    duplicates = list()
    for name, info in files.items():
        if len(info) > 1:
            # print(files[name])
            options = sorted(files[name], key=region_sort)
            # print(name, options)
            for option in options[1:]:
                duplicates.append(str(option))
    return duplicates


def find_files(path):
    file_info = defaultdict(list)
    for root, _, files in os.walk(path):
        for file in files:
            result = FILE_REGEXP.match(file)
            if result:
                name = result.group(1)
                region = result.group(2).strip()
                file_info[name].append(FileInfo(name, region, file, root))
    return file_info


if __name__ == '__main__':
    main()
