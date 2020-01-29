from typing import Iterable, List, Callable


def is_from_same(itr):
    itr = list(itr)
    if len(itr) == 0:
        return True
    model = itr[0]
    for el in itr[1:]:
        if model != el:
            return False
    return True


# def isiterable(obj):
#     return hasattr(obj, '__iter__')


def uncover(obj) -> List:
    def uncover_rec(sub_obj):
        if isinstance(sub_obj, (list, tuple)):
            for el in sub_obj:
                uncover_rec(el)
        else:
            res.append(sub_obj)
    res = []
    uncover_rec(obj)
    return res


class ListMcPolymorph:
    """Понимайте это как хотите"""
    def __init__(self, init_val, val_appending: Callable):
        self.val = init_val
        self.val_appending = val_appending

    def add(self, what):
        self.val_appending(self.val, what)


class UsefulObj:
    args_trick = []

    def __init__(self, *args, **kwargs):
        for p in range(len(args)):
            setattr(self, self.args_trick[p], args[p])
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def import_from_parent(self, pr_obj, *args):
        # Ну, это хотя бы лучше, чем было
        keys: Iterable = uncover(args)
        for key in keys:
            val = getattr(pr_obj, key, None)
            setattr(self, key, val)
