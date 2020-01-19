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
        # пффффф
        if names is None:
            self.names = std_names
        else:
            self.names = names
        if specific_operators is None:
            self.specific_operators = std_specific_operators
        else:
            self.specific_operators = specific_operators
        self.pare_brackets = ["()", "{}"]

        # execution levels)))
        self.execution_levels = set()
        for name in self.names:
            if self.names[name]["type"] == "op":
                self.execution_levels.add(self.names[name]["level"])
        self.execution_levels = sorted(list(self.execution_levels), reverse=True)

        # specific_symbols
        self.specific_chars = set()
        for name in self.specific_operators:
            for ch in name:
                self.specific_chars.add(ch)

    def comp_exp(self, query):
        return ExpEvalProcedure(self, query)()


class ExpEvalProcedure:
    def __init__(self, config: ExpEval, query):
        self.config = config
        self.query = query
        self.tokens = []

    @staticmethod
    def is_latin(char: str):
        char = ord(char.lower())
        return ord("a") <= char <= ord("z")

    @staticmethod
    def is_digit(char: str):
        return ord("0") <= ord(char) <= ord("9")

    def split_to_tokens(self):
        """The most boring part (i hope)"""
        for p in range(len(self.query)):
            ch: str = self.query[p]

    def __call__(self):
        self.query += "\x00"
        self.split_to_tokens()
