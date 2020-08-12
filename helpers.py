from functools import reduce


def compose(*funcs):
    def _compose(f, g):
        def compose_(x):
            return f(g(x))
        return compose_
    return reduce(_compose, funcs)


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start
