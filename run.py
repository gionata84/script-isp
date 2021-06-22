import shutil

from base import GitClone
import sys
import os
import re
import time



folder_common = 'tmp_common'
folder_target = 'target_repo/tmp/'


def main(argv):

    common_repo = GitClone('demo-common', folder_common)
    common_repo.close()

    target_repo = GitClone('foo', folder_target)

    for config_file in os.listdir(folder_common + '/configurations'):
        target_repo.switch_branch(os.path.splitext(config_file)[0])
        values = build_phs(config_file)
        for filename in os.listdir(folder_common):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                with open(folder_common + '/' + filename, 'r') as instream:
                    content = instream.read()
                    content = re.sub("\${(.*?)}", replace_var(values), content)
                    print(filename)
                    outF = open(folder_target + "/" + filename, "w")
                    outF.write(content)
                    outF.close()

        #add, create branch and push
        target_repo.push_branch(os.path.splitext(config_file)[0])
        #clean_folder()

    target_repo.close()


def clean_folder():
    print('#######################')
    for file in os.listdir(folder_target):
        print(file)
        if file.endswith(".yml") or file.endswith(".yaml"):
            join = os.path.join(folder_target, file)
            print(join)
            os.remove(join)


def move_files(source_dir, target_dir):
    touple = ['.yml', '.yaml']
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        name, extension = os.path.splitext(file_name)
        if extension in touple:
            shutil.move(os.path.join(source_dir, file_name), target_dir)


def replace_var(values):
    def lookup(match):
        key = match.group(1)
        return values.get(key, f'<{key} not found>')

    return lookup


def build_phs(config):
    d = {}
    with open(folder_common + '/configurations/' + config) as f:
        for line in f:
            (key, val) = line.split(':')
            d[(key.strip())] = val.strip()

    with open('inputs/input_1') as f:
        for line in f:
            (key, val) = line.split()
            d[(key.strip())] = val.strip()
    return d


if __name__ == "__main__":
    main(sys.argv[1:])
