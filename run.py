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
    for filename in os.listdir(folder_common):
        if filename.endswith(".yml"):
            with open(folder_common + '/' + filename, 'r') as instream:
                content = instream.read()
                content = re.sub("\${(.*?)}", replace_var, content)
                outF = open(target_folder + "/" + filename, "w")
                outF.write(content)
                outF.close()



def templating_target(env):
    folder_common = 'tmp_common_' + env
    folder_out = 'tmp_out' + env
    os.makedirs(folder_common)
    os.makedirs(folder_out)
    master = git.Repo.clone_from('https://github.com/gionata84/demo-common.git', folder_common, branch='main')
    master.close()
    for filename in os.listdir(folder_common):
        if filename.endswith(".yml"):
            with open(folder_common + '/' + filename, 'r') as instream:
                content = instream.read()
                content = re.sub("\${(.*?)}", replace_var, content)
                outF = open(folder_out + "/" + filename, "w")
                outF.write(content)
                outF.close()


def replace_var(match):
    var = match.group(1)
    values = create_values()
    if var in values:
        return values[var]


def create_values():
    d = {}
    with open('inputs/input_1') as f:
        for line in f:
            (key, val) = line.split()
            d[(key)] = val
    return d


if __name__ == "__main__":
    main(sys.argv[1:])
