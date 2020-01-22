import math
from typing import Tuple, Callable


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


class CalcUbotName:
    type: str

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])


class CalcUbotVal(CalcUbotName):
    val = None


class Operator(CalcUbotName):
    level: int
    sides: Tuple[bool, bool, bool]
    func: Callable


class CharOperator(CalcUbotName):
    replace: str
    allow_shuffle: bool
    from_heaven = None
    branching: bool


class Namespace(CalcUbotName):
    cont: dict


std_names = {
    "pi": {
        "type": "int",
        "val": math.pi
    },
    "comb": {
        "type": "namespace",
        "cont": {
            "comb_c": {
                "type": "func",
                "val": cnpk
            }
        }
    },
    "__addition__": {
        "type": "op",
        "level": 1,
        "sides": (True, False, True),
        "func": lambda a, b, c: a + b * c
    },
    "__fact__": {
        "type": "op",
        "level": 3,
        "sides": (True, False, False),
        "func": math.factorial
    },
    "mod": {
        "type": "op",
        "level": 4,
        "sides": (True, True, True),
        "func": lambda a, bl, c: a % bl[0] == c % bl[0]
    }
}

std_specific_operators = {
    "+": {
        "replace": "__addition__",
        "allow_shuffle": False,
        "from_heaven": [1],
        "branching": True
    },
    "-": {
        "replace": "__addition__",
        "allow_shuffle": False,
        "from_heaven": [-1],
        "branching": True
    },
    "!": {
        "replace": "__fact__",
        "allow_shuffle": False,
        "from_heaven": [],
        "branching": False
    }
}
