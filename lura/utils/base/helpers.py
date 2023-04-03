#!/usr/bin/python3

def register(func):
    def inner(plugin, *args, **kwargs):
        key=f'{plugin.__class__.__name__}_{func.__name__}'
        plugin.app.actions[key]=func
        return func(plugin, *args, **kwargs)
    return inner
