import os
import git
import shutil

from plug import Plug, tag

class Picky(Plug):

    base='https://github.com'

    def setup(self):
        super().setup()
        self.addPicksFolder()
        self.loadPicks()

    def addPicksFolder(self):
        plugman_folder=self.app.plugman.folder
        path=os.path.join(plugman_folder, 'picky')
        self.folder=self.app.createFolder(path)

    def loadPicks(self, picks=[]):
        modules=[]
        picks=picks or self.getPicks()
        for pick in picks:
            repo=pick['repo']
            path=os.path.join(self.folder, repo)
            if not os.path.exists(path):
                continue
            modules+=[repo]
            git_repo=git.Repo(path)
            pick['git_repo']=git_repo
            if not git_repo.bare:
                self.checkoutToBranch(pick)
                self.checkoutToCommit(pick)
        self.app.plugman.loadPlugs(
                folder=self.folder, modules=modules)

    def checkoutToBranch(self, pick):
        git_repo=pick['git_repo']
        branch=pick.get('branch', None)
        if not branch:
            git_repo.heads[0].checkout()
            return
        for head in git_repo.branches:
            if head.name!=branch:
                continue
            head.checkout()
            return

    def checkoutToCommit(self, pick):
        git_repo=pick['git_repo']
        commit=pick.get('commit', None)
        if not commit:
            return
        for head in git_repo.iter_commits():
            if head.hexsha!=commit:
                continue
            git_repo.git.checkout(head)
            return

    def getPicks(self):
        plugs=[]
        picks = self.m_config.get("Picks", [])
        for pick in picks:
            if type(pick)==str:
                pick=dict(plug=pick)
            if not 'base' in pick:
                pick['base']=self.base
            plug=pick.get('plug')
            _, repo = tuple(plug.split("/"))
            pick['repo']=repo
            plugs.append(pick)
        return plugs

    @tag(["(exec)", "<c-P>I(normal)"])
    def installPicks(self):
        modules=[]
        picks=self.getPicks()
        for pick in picks:
            repo=pick['repo']
            plug=pick['plug']
            base = os.path.expanduser(pick["base"])
            path=os.path.join(self.folder, repo)
            if os.path.exists(path):
                continue
            if os.path.exists(base):
                repo_path=os.path.join(base, repo)
                shutil.copy(repo_path, path)
            else:
                url = f"{base}/{plug}"
                git.Repo.clone_from(url, path)
            modules+=[pick]
        self.loadPicks(modules)

    @tag(["(exec)", "<c-P>U(normal)"])
    def updatePicks(self):
        for repo in os.listdir(self.folder):
            path = os.path.join(self.folder, repo)
            git_repo = git.Repo(path)
            if git_repo.bare:
                continue
            for remote in git_repo.remotes:
                remote.pull()
        self.loadPicks()

    @tag(["(exec)", "<c-P>C(normal)"])
    def cleanupPicks(self):
        picks=self.getPicks()
        repos=[p['repo'] for p in picks]
        for repo in os.listdir(self.folder):
            if repo in repos: continue
            path = os.path.join(self.folder, repo)
            if os.path.islink(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
