import math


__all__ = ["std_names", "std_specific_operators"]


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


# TODO: optimize this bullshit
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
                "calc": cnpk
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
        "allow_shuffle": False,  # Bad example
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
