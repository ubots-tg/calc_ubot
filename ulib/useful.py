def is_from_same(itr):
    itr = list(itr)
    if len(itr) == 0:
        return True
    model = itr[0]
    for el in itr[1:]:
        if model != el:
            return False
    return True


class UsefulObj:
    args_trick = []

    def __init__(self, *args, **kwargs):
        for p in range(len(args)):
            setattr(self, self.args_trick[p], args[p])
        for k in kwargs:
            setattr(self, k, kwargs[k])
