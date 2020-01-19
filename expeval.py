import threading
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
        self.other_symbols = list("(){},;")  # They all 1 char length

        # execution levels)))
        self.execution_levels = set()
        for name in self.names:
            if self.names[name]["type"] == "op":
                self.execution_levels.add(self.names[name]["level"])
        self.execution_levels = sorted(list(self.execution_levels), reverse=True)

        # operator_symbols
        self.operator_symbols = set()
        for name in self.specific_operators:
            for ch in name:
                self.operator_symbols.add(ch)

    def comp_exp(self, query):
        try:
            return ExpEvalProcedure(self, query)()
        except Exception as err:
            return err, False


class ExpEvalProcedure:
    def __init__(self, config: ExpEval, query):
        self.config = config
        self.query = query
        # Tokenizer
        self.char_map = [-1] * len(query)
        self.checks = [
            self.is_latin,
            self.is_digit,
            lambda ch: ch.isspace(),
            lambda ch: ch in self.config.operator_symbols,
            lambda ch: ch == "\x00",
            lambda ch: ch in self.config.other_symbols
        ]
        self.tokens = []

    def get_ch(self, p) -> str:
        if 0 <= p < len(self.query):
            return "\x00"
        return self.query[p]

    @staticmethod
    def is_latin(char: str):
        char = ord(char.lower())
        return ord("a") <= char <= ord("z")

    @staticmethod
    def is_digit(char: str):
        return ord("0") <= ord(char) <= ord("9")

    def split_to_tokens(self):
        """
        The most boring part (i hope)
        0 - word letter
        1 - digit
        2 - space
        3 - operator symbol
        4 - \x00
        5 - other symbols
        6 - innocent symbol -> error
        """
        for p in range(len(self.query)):
            ch = self.get_ch(p)
            for i in range(len(self.checks)):
                if self.checks[i](ch):
                    self.char_map[p] = i
                    break
            else:
                raise Exception("Innocent symbol %s at pos %d" % (ch, p + 1))

    def __call__(self):
        self.query += "\x00"
        self.split_to_tokens()
