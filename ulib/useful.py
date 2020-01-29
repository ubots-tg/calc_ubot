from typing import Iterable, List


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
        # print(sub_obj)
        if isinstance(sub_obj, (list, tuple)):
            for el in sub_obj:
                uncover_rec(el)
        else:
            # print("db|u,")
            res.append(sub_obj)
    res = []
    uncover_rec(obj)
    return res


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
