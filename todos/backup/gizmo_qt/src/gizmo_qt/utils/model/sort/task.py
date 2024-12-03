import threading
from queue import Queue

from PyQt6 import QtCore

from .utils import SortMatch, SortRegex


class SortFilterTask(QtCore.QObject):
    ready = QtCore.pyqtSignal(object, object)

    def __init__(self, source):
        super().__init__()
        self.m_state = {}
        self.m_min_score = 25
        self.m_current = None
        self.m_running = False
        self.m_source = source
        self.m_queue = Queue()
        self.m_regex = SortRegex
        self.m_matcher = SortMatch
        self.m_ext = getattr(source, "m_ext", "")

        if self.m_source.app:
            q = self.m_source.app.appSoonQuits
            q.connect(self.stop)

    def stop(self):
        self.m_running = False
        self.m_queue.put(None)

    def start(self, regex_id):
        self.m_current = regex_id
        c = self.m_state.get(regex_id, 0)
        self.m_queue.put((c, regex_id))

    def run(self):
        self.m_running = True

        def leep():
            while self.m_running:
                data = self.m_queue.get()
                if data is None:
                    return
                alist = []
                c, rid = data
                path, rgx = rid
                rr, urgx = self.m_regex(rgx)
                cache = self.m_source.getRootData(root=path)
                (
                    count,
                    canFetch,
                    ipath,
                    flist,
                ) = cache
                while self.m_running:
                    to_break = False
                    if c >= count:
                        if ipath.hasNext():
                            self.m_source.fetchMore(
                                root=path,
                                limit=15000,
                            )
                            cache = (
                                self.m_source.getRootData(
                                    root=path
                                )
                            )
                            (
                                count,
                                canFetch,
                                ipath,
                                flist,
                            ) = cache
                        else:
                            break
                    else:
                        for i in range(15000):
                            if self.m_current != rid:
                                self.m_queue.put((c, rid))
                                to_break = True
                                break
                            if c < count:
                                p = flist[c]
                                c += 1
                            else:
                                break
                            pp = p.lower()
                            if p.lower().endswith(
                                self.m_ext
                            ):
                                s = self.m_matcher(
                                    urgx, rr, pp
                                )
                                if s > self.m_min_score:
                                    alist += [(p, s)]
                            if len(alist) > 500:
                                self.ready.emit(rid, alist)
                                alist = []
                        if not alist:
                            continue
                        self.ready.emit(rid, alist)
                        alist = []
                        if to_break:
                            break
                canFetch = ipath.hasNext()
                cache = (
                    count,
                    canFetch,
                    ipath,
                    flist,
                )
                self.m_source.m_cache[path] = cache
                if alist:
                    self.ready.emit(rid, alist)

        t = threading.Thread(target=leep)
        t.deamon = True
        t.start()
