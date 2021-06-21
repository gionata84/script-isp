import git
import sys
import os
import re

folder_common = 'tmp_common'


def main(argv):
    os.makedirs(folder_common)
    master = git.Repo.clone_from('https://github.com/gionata84/demo-common.git', folder_common, branch='main')
    master.close()
    for filename in os.listdir(folder_common + '/configurations'):
        execute(filename)


def execute(filename):
    target_folder = 'target/' + os.path.splitext(filename)[0]
    os.makedirs(target_folder)
    values = build_phs(filename)
    for filename in os.listdir(folder_common):
        if filename.endswith(".yml"):
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
