import math
from expeval_funcs import *

# TODO: optimize this bullshit
std_names = {
    "pi": {
        "type": "int",
        "val": math.pi
    },
    "__addition__": {
        "type": "op",
        "level": 1,
        "sides": (1, 1),
        "func": addition
    },
    "__plus-minus__": {
        "type:": "op",
        "level": 1,
        "sides": (1, 1),
        "func": make_set_plus_minus
    }
}

std_specific_operators = {
    "+": {
        "replace": "__addition__",
        "from_heaven": [1]
    },
    "-": {
        "replace": "__addition__",
        "from_heaven": [-1]
    },
    "+-": {
        "allow_shuffle": True,
        "replace": "__plus-minus__"
    }
}


class ExecutionPoint:
    pass


class Token:
    def __init__(self, token, word=False, val=False):
        self.token = token
        self.word = word
        self.val = val


class ExpEval:
    def __init__(self, names=None, specific_operators=None):
        if names is None:
            self.names=std_names
        else:
            self.names = names
        if specific_operators is None:
            self.specific_operators=std_specific_operators
        else:
            self.specific_operators = specific_operators
        self.pare_brackets = ["()", "{}"]

    def comp_exp(self, query):
        return ExpEvalProcedure(self, query)()


class ExpEvalProcedure:
    def __init__(self, config: ExpEval, query):
        self.config = config
        self.query = query

    def __call__(self):
        for p in range(len(self.query)):
            ch = self.query[p]

