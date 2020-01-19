def addition(a, b, c):
    return a + b * c


def make_set_plus_minus(a, b):
    res = set()
    res.add(a + b)
    res.add(a - b)
    return res
