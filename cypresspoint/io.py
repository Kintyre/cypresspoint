import gzip


def openany(fn):
    if fn.endswith(".gz"):
        return gzip.open(fn)
    else:
        return open(fn)
