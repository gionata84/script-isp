import shutil

import git
import sys
import os
import re

folder_common = 'tmp_common'
folder_target = 'target_repo/tmp'


def main(argv):
    os.makedirs(folder_common)
    common_repo = git.Repo.clone_from('https://github.com/gionata84/demo-common.git', folder_common, branch='main')
    common_repo.close()

    os.makedirs(folder_target)
    target_repo = git.Repo.clone_from('https://gionata84:Arancia0!@github.com/gionata84/foo.git', folder_target, branch='main')

    for config_file in os.listdir(folder_common + '/configurations'):
        values = build_phs(config_file)
        for filename in os.listdir(folder_common):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                with open(folder_common + '/' + filename, 'r') as instream:
                    content = instream.read()
                    content = re.sub("\${(.*?)}", replace_var(values), content)
                    outF = open(folder_target + "/" + filename, "w")
                    outF.write(content)
                    outF.close()

        #add, create branch and push
        env = os.path.splitext(config_file)[0]
        target_repo.git.checkout('HEAD', b=env)
        target_repo.git.add(all=True)
        target_repo.index.commit('start ' + env)
        origin = target_repo.remote(name='origin')
        target_repo.git.push("--set-upstream", origin, target_repo.head.ref)
        origin.push()
        clean_folder()

    clean_folder()
    target_repo.close()


def clean_folder():
    for item in folder_target:
        if item.endswith(".yml") or item.endswith(".yaml"):
            os.remove(os.path.join(folder_target, item))


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
