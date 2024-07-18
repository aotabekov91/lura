import os
import git
import shutil

from plug import Plug, tag

class Picky(Plug):

    base='https://github.com/'

    def setup(self):
        super().setup()
        self.addPicksFolder()
        self.loadPicks()

    def addPicksFolder(self):
        plugman_folder=self.app.plugman.folder
        path=os.path.join(plugman_folder, 'picky')
        self.folder=self.app.createFolder(path)

    def loadPicks(self):
        modules=[]
        picks=self.getPicks()
        for pick in picks:
            repo=pick['repo']
            path=os.path.join(self.folder, repo)
            if os.path.exists(path):
                modules+=[pick['repo']]
        self.app.plugman.loadPlugs(
                folder=self.folder,
                modules=modules)

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

    def installRepo(self, repo, base=None):
        name, path, folder = self.updateInfo(repo)
        self.plugs[name] = folder
        base = base or self.base
        if not name in self.repos:
            self.repos += [name]
        if not os.path.exists(path):
            gpath = os.path.expanduser(repo)
            if os.path.exists(gpath):
                shutil.copy(gpath, path)
            else:
                url = f"{base}/{repo}"
                git.Repo.clone_from(url, path)
        return name, folder

    @tag("(exec)")
    def installPicks(self):
        self.getPicks()
        picks = self.m_config.get("Picks", [])
        for data in picks:
            repo = data.get("pick", None)
            base = data.get("base", None)
            if not repo:
                continue
            self.installRepo(repo, base)

    @tag("(exec)")
    def updatePicks(self):
        for name in self.repos:
            p = os.path.join(self.folder, name)
            repo = git.Repo(p)
            repo.remotes.origin.pull()

    @tag("(exec)")
    def cleanupPicks(self):
        for d in os.listdir(self.folder):
            if not d in self.repos:
                p = os.path.join(self.folder, d)
                shutil.rmtree(p)
