import math
from typing import Tuple, Callable


class CalcUbotName:
    type: str

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


class Operator(CalcUbotName):
    type = "op"
    level: int
    sides: Tuple[bool, bool, bool]
    func: Callable


class CharOperator(CalcUbotName):
    type = "__non_name_char_op__"  # Crutch
    replace: str
    allow_shuffle = False
    from_heaven = []
    branching = True


class Namespace(CalcUbotName):
    type = "ns"
    cont: dict

    def apply_path(self, path: str):
        sp_res = path.split(".", 1)
        in_me = self.cont[sp_res[0]]
        if len(sp_res) == 1:
            return in_me
        return in_me.apply_path(sp_res[1])

    def __iter__(self):
        return self.cont.__iter__()

    def __getitem__(self, item: str):
        return self.apply_path(item)


def cnpk(n, k):
    res = 1
    for u in range(n, n - k, -1):
        res *= u
    res //= math.factorial(k)
    return res


def exgcd(a, b):
    if b == 0:
        return 1, 0, a
    y, x, gcd = exgcd(b, a % b)
    return x, y - (a // b) * x, gcd


std_names = Namespace(cont={
    "comb": Namespace(cont={
        "comb_c": cnpk
    }),
    "pi": math.pi,
    "__addition__": Operator(level=1, sides=(True, False, True), func=lambda a, b, c: a + b * c),
    "__fact__": Operator(level=3, sides=(True, False, False), func=math.factorial),
    "mod": Operator(level=1, sides=(True, True, True), func=lambda a, bl, c: a % bl[0] == c % bl[0])
})

std_specific_operators = {
    "+": CharOperator(replace="__addition__", from_heaven=[1]),
    "-": CharOperator(replace="__addition__", from_heaven=[-1]),
    "!": CharOperator(replace="__fact__", branching=False),
}
