import os
import git
import shutil

from plug import Plug, tag, deleg

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
            folder=pick['folder']
            pick_path=os.path.join(self.folder, folder)
            if os.path.exists(pick_path):
                modules+=[pick]
                try:
                    git_repo=git.Repo(pick_path)
                    pick['git_repo']=git_repo
                    if not git_repo.bare:
                        branch=pick.get('branch', None)
                        if branch:
                            self.setBranch(branch, git_repo)
                        commit=pick.get('commit', None)
                        if commit:
                            self.setCommit(commit, git_repo)
                except git.exc.InvalidGitRepositoryError:
                    pick['git_repo']=None
        self.app.plugman.loadPlugs(
                folder=self.folder, modules=modules)

    @deleg('getPickyFolder@(normal){Picky}')
    def getFolder(self):
        return self.folder

    @deleg('getPicks@(normal){Picky}')
    def getPicks(self):
        plugs=[]
        picks = self.m_config.get('Picks', []) # todo or []
        picks = picks or []
        for pick in picks:
            if type(pick)==str:
                pick=dict(plug=pick)
            if not 'base' in pick:
                pick['base']=self.base
            plug=pick.get('plug')
            pick['folder']=plug.split("/")[1]
            plugs.append(pick)
        return plugs

    def setBranch(self, branch, git_repo):
        if branch:
            for head in git_repo.branches:
                if head.name==branch:
                    return head.checkout()

    def setCommit(self, commit, git_repo):
        if commit:
            for head in git_repo.iter_commits():
                if head.hexsha==commit:
                    return git_repo.git.checkout(head)

    @tag("(exec)")
    def PickyInstall(self):
        modules=[]
        picks=self.getPicks()
        for pick in picks:
            plug=pick['plug']
            base=pick['base']
            folder=pick['folder']
            pick_base = os.path.expanduser(base)
            path=os.path.join(self.folder, folder)
            if not os.path.exists(path):
                if os.path.exists(pick_base):
                    pick_path=os.path.join(pick_base, plug)
                    if os.path.exists(pick_path):
                        kind=pick.get('kind', 'copy')
                        if kind=='copy':
                            shutil.copytree(pick_path, path)
                        elif kind=='link':
                            os.symlink(pick_path, path)
                else:
                    url = f"{pick_base}/{plug}"
                    try:
                        git.Repo.clone_from(url, path)
                    except:
                        continue
                modules+=[pick]
        self.loadPicks(modules)

    @tag("(exec)")
    def PickyUpdate(self):
        for repo in os.listdir(self.folder):
            path = os.path.join(self.folder, repo)
            try:
                git_repo = git.Repo(path)
                for remote in git_repo.remotes:
                    remote.pull()
            except git.exc.InvalidGitRepositoryError:
                pass
        self.loadPicks()

    @tag("(exec)")
    def PickyCleanup(self):
        picks=self.getPicks()
        repos=[pick['folder'] for pick in picks]
        for repo in os.listdir(self.folder):
            if not repo in repos: 
                pick_path = os.path.join(self.folder, repo)
                plugs=self.app.plugman.getPlug(path=pick_path)
                for plug in plugs:
                    if plug: plug.tearup()
                if os.path.islink(pick_path):
                    os.unlink(pick_path)
                else:
                    shutil.rmtree(pick_path)
