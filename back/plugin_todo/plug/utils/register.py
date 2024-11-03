def register(key=None, info=None, modes=[], command=True):

    def _key(func):

        def inner(self, *args, **kwargs): return func(self, *args, **kwargs)
        inner.key=key
        inner.info=info
        inner.modes=modes
        inner.func=func
        inner.command=command
        inner.name=func.__name__
        return inner

    return _key
