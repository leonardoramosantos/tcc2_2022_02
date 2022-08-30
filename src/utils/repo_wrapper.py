from abc import ABC, abstractmethod

class RepoWrapper(ABC):
    def __init__(self, repo_path, repo_last_commit):
        self.repo_path = repo_path
        self.repo_last_commit = repo_last_commit

    @abstractmethod
    def udpate_repo(self):
        pass