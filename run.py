import git
import sys
import os
import re


def main(argv):
    templating_target('dev')
    templating_target('prod')


def templating_target(env):
    folder_origin = 'tmp_common_' + env
    folder_out = 'tmp_out' + env
    os.makedirs(folder_origin)
    os.makedirs(folder_out)
    master = git.Repo.clone_from('https://github.com/gionata84/demo-common.git', folder_origin, branch=env)
    master.close()
    for filename in os.listdir(folder_origin):
        if filename.endswith(".yml"):
            with open(folder_origin + '/' + filename, 'r') as instream:
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
