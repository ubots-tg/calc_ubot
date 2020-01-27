import math
from typing import Tuple, Callable, List
from ulib.useful import UsefulObj


class Operator(UsefulObj):
    level: int
    sides: Tuple[bool, bool, bool]
    func: Callable
    rev: bool = False  # For executor


class CharOperator(UsefulObj):
    replace: str
    allow_shuffle = False
    from_heaven = []
    branching = True


class CompOperator(UsefulObj):
    branches: List[Operator]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.branches[0]

    def get_level(self):
        return min(map(lambda op: op.level, self.branches))


class Namespace(UsefulObj):
    cont: dict

    def apply_path(self, path: str):
        sp_res = path.split(".", 1)
        in_me = self.cont[sp_res[0]]
        if len(sp_res) == 1:
            if isinstance(in_me, Operator):
                return CompOperator(branches=[in_me])
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
    "mod": Operator(level=1, sides=(True, True, True), func=lambda a, bl, c: a % bl[0] == c % bl[0]),
    "sqrt": math.sqrt,
    "__multiplication__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a * b),
    "__division__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a / b)
})

std_specific_operators = {
    "+": CharOperator(replace="__addition__", from_heaven=[1]),
    "-": CharOperator(replace="__addition__", from_heaven=[-1]),
    "!": CharOperator(replace="__fact__", branching=False),
    "*": CharOperator(replace="__multiplication__"),
    "/": CharOperator(replace="__division__")
}
