#python2.7
from git import *
import os

class gitUity:

    #init need repo path
    def __init__(self,repoDir,repoName):
        self.repoName = repoName
        self.repoDir = repoDir
        if not os.path.exists(repoDir+'/'+repoName):
            os.makedirs(repoDir+'/'+repoName)
        else:
            self.repo = Repo(os.path.join(repoDir,repoName))
        self.branch = 'master'

    def status(self):
        return self.repo.status()

    def setRemote(self,rName,remote):
        self.repo.add.remote(Name,remote)

    def clone(self,remote):
        self.clone(remote,'')

    def clone(self,remote):
        self.remote = remote
        self.repo = Repo.clone_from(remote,os.path.join(self.repoDir,self.repoName))

    def pull(self):
        self.repo.pull(self.remote,self.branch)

    def autoCommit(self):
        self.repo.commit('-a','-m','auto commit')

