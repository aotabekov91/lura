import shlex
import argparse


class Parser:
    def __init__(self, *args, **kwargs):
        self.setup()

    def setup(self):
        self.setParser()
        self.m_subparsers = {}

    def addArgument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def newArgParser(self, *args, **kwargs):
        return Parser(*args, **kwargs)

    def newParser(self, *args, **kwargs):
        return argparse.ArgumentParser(**kwargs)

    def setParser(self, **kwargs):
        self.parser = self.newParser(
            exit_on_error=False, **kwargs
        )

    def addSubParser(self, *args, **kwargs):
        return self.parser.add_subparsers(*args, **kwargs)

    def split(self, text):
        return shlex.split(text)

    def parse(
        self,
        text=None,
        pref=None,
        only_known=True,
    ):
        f = self.parser.parse_args
        if only_known:
            f = self.parser.parse_known_args
        if text:
            t = shlex.split(text)
            if pref:
                t.insert(0, pref)
            return f(t)
        return f()
