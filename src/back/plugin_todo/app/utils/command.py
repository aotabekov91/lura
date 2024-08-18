import os
import time

def os_command(delay=None, wait=None):
    def command(func):
        def inner(self, *args, **kwargs):
            if delay: time.sleep(delay)
            cmd = func(self, *args, **kwargs)
            if cmd: os.popen(cmd)
            if wait: time.sleep(wait)
        return inner
    return command
