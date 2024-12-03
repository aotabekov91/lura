def dict_factory(c, r):

    d = {}
    for idx, col in enumerate(c.description):
        d[col[0]] = r[idx]
    return d
