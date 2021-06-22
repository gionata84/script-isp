import shutil

import git
import sys
import os
import re

folder_common = 'tmp_common'
target_repo = 'target_repo/'


def main(argv):
    os.makedirs(folder_common)
    master = git.Repo.clone_from('https://github.com/gionata84/demo-common.git', folder_common, branch='main')
    master.close()
    for config_file in os.listdir(folder_common + '/configurations'):
        #create tmp folder target
        execute(config_file)

        #create final folder target
        env = os.path.splitext(config_file)[0]
        os.makedirs(target_repo + env)
        repo = git.Repo.clone_from('https://gionata84:Arancia0!@github.com/gionata84/foo.git', target_repo + env)

        #move file form tmp to final
        move_files('target/' + env, target_repo + env)

        #add, create branch and push
        repo.git.checkout('HEAD', b=env)
        repo.git.add(all=True)
        repo.index.commit('start ' + env)
        origin = repo.remote(name='origin')
        repo.git.push("--set-upstream", origin, repo.head.ref)
        origin.push()


def move_files(source_dir, target_dir):
    touple = ['.yml', '.yaml']
    file_names = os.listdir(source_dir)

    for file_name in file_names:
        name, extension = os.path.splitext(file_name)
        if extension in touple:
            shutil.move(os.path.join(source_dir, file_name), target_dir)


def execute(config_file):
    target_folder = 'target/' + os.path.splitext(config_file)[0]
    os.makedirs(target_folder)
    values = build_phs(config_file)
    for filename in os.listdir(folder_common):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            with open(folder_common + '/' + filename, 'r') as instream:
                content = instream.read()
                content = re.sub("\${(.*?)}", replace_var(values), content)
                outF = open(target_folder + "/" + filename, "w")
                outF.write(content)
                outF.close()


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
