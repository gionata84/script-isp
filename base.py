import git
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
git_config = config['git']


class GitClone:

    def __init__(self, repo_name, repo_dir, from_branch=''):
        self.repo_user = git_config['user']
        self.repo_pass = git_config['password']
        self.repo_name = repo_name
        repo_url = '{0}://{1}:{2}@github.com/{1}/{3}.git'
        self.repo_url = repo_url.format(git_config['protocol'], self.repo_user, self.repo_pass, self.repo_name)
        self.repo_dir = repo_dir or self.repo_name
        self.from_branch = from_branch or 'main'
        self.branch = self.from_branch
        self.repo = git.Repo.clone_from(self.repo_url, self.repo_dir, branch=self.from_branch)

    def close(self):
        self.repo.close()

    def push_branch(self, branch):
        self.repo.git.add(all=True)
        self.repo.index.commit('start ' + branch)
        origin = self.repo.remote(name='origin')
        self.repo.git.push("--set-upstream", origin, self.repo.head.ref)
        origin.push()

    def switch_branch(self, param):
        self.repo.git.checkout('main')
        self.repo.git.checkout(b=param)
