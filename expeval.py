from typing import List, Tuple
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
        "from_heaven": [1],
        "branching": True
    },
    "-": {
        "replace": "__addition__",
        "from_heaven": [-1],
        "branching": True
    }
}


class ExecutionPoint:
    pass


class Token:
    def __init__(self, token, word=False, val=False, op=False):
        """Crutch"""
        self.token = token
        self.word = word
        self.val = val
        # Operators stuff
        self.op = op
        self.finished = False
        self.reversed = False


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
        self.other_symbols = list("(){},;.")  # They all 1 char length
        self.pares = {"<": ">"}

        # execution levels)))
        self.execution_levels = set()
        for name in self.names:
            if self.names[name]["type"] == "op":
                self.execution_levels.add(self.names[name]["level"])
        self.execution_levels = sorted(list(self.execution_levels), reverse=True)

        # operator_symbols
        self.operator_symbols = set()
        for name in list(self.specific_operators.keys()) + list(self.pares.keys()):
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
        self.tokenizer = Tokenizer(self, self.query)
        self.tokens: List[Token] = []

    def __call__(self):
        self.tokenizer()


class Tokenizer:
    def __init__(self, procedure: ExpEvalProcedure, query):
        self.procedure = procedure
        self.query = query + "\x00"
        self.char_types = [-1] * (len(self.query))
        self.checks = [
            self.is_latin,
            self.is_digit,
            lambda ch: ch.isspace(),
            lambda ch: ch in self.procedure.config.operator_symbols,
            lambda ch: ch == "\x00",
            lambda ch: ch in self.procedure.config.other_symbols
        ]
        self.tokens: List[Token] = []

    def get_ch(self, p) -> Tuple[str, int]:
        if 0 <= p < len(self.query):
            ch = self.query[p]
            if self.char_types[p] == -1:
                for i in range(len(self.checks)):
                    if self.checks[i](ch):
                        self.char_types[p] = i
                        break
                else:
                    raise Exception("Innocent symbol %s at pos %d" % (ch, p + 1))
        else:
            return "\x00", 4
        return ch, self.char_types[p]

    @staticmethod
    def is_latin(char: str):
        char = ord(char.lower())
        return ord("a") <= char <= ord("z")

    @staticmethod
    def is_digit(char: str):
        return ord("0") <= ord(char) <= ord("9")

    def simplify_the_operator(self, operator):
        rev = False
        for i in range(len(operator)):
            ch = operator[i]
            if ch in self.procedure.config.pares:
                rev = True
                operator[i] = self.procedure.config.pares[ch]
        return sorted(operator), rev

    def is_finished_operator(self, my_op):
        simple_my_op, rev = self.simplify_the_operator(my_op)
        for op in self.procedure.config.specific_operators:
            if self.simplify_the_operator(op)[0] == simple_my_op:
                return simple_my_op, rev
        return False, False

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
            ch1, tp1 = self.get_ch(p)
            ch2, tp2 = self.get_ch(p - 1)
            if tp1 == 5:
                self.tokens.append(Token(ch1))
                continue
            if tp1 in (2, 4):
                continue
            if tp1 == tp2:
                if tp1 == 3:
                    if not self.tokens[-1].finished:
                        self.tokens[-1].token += ch1
                else:
                    self.tokens[-1].token += ch1
            else:
                self.tokens.append(Token(ch1))
                if tp1 == 0:
                    self.tokens[-1].word = True
                if tp1 == 1:
                    self.tokens[-1].val = True
                if tp1 == 3:
                    self.tokens[-1].op = True
            if tp1 == 3:
                simple_op, rev = self.is_finished_operator(self.tokens[-1].token)
                if simple_op:
                    self.tokens[-1].token = simple_op
                    self.tokens[-1].finished = True
                    self.tokens[-1].reversed = rev

    def __call__(self):
        self.split_to_tokens()
        self.procedure.tokens = self.tokens
