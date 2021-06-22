from git import Repo


class GitClone:
    def __init__(self, repo_owner, repo_name, repo_dir=None, do_clone=True, from_branch=''):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        repo_url = 'https://github.com/{0}/{1}'
        self.repo_url = repo_url.format(self.repo_owner, self.repo_name)
        self.repo_dir = repo_dir or self.repo_name
        # by default, start on master.
        self.from_branch = from_branch or 'master'
        self.branch = self.from_branch
        if do_clone:
            self.repo = Repo.clone_from(
                self.repo_url, self.repo_dir, branch=self.from_branch)
        else:
            self.repo = Repo(repo_dir)
        self.git = self.repo.git
