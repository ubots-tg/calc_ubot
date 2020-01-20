from typing import List, Tuple
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


class Token:
    def __init__(self, token, st=-1, word=False, val=False, op=False):
        """Crutch"""
        self.token = token
        self.st = st
        self.word = word
        self.val = val
        self.op = op
        self.rev = False


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
        self.other_symbols = list("()[]{},;.")  # They all 1 char length
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

        # max operator size
        self.mx_op_size = max(map(lambda n: len(n), self.specific_operators.keys()))

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
                self.tokens.append(Token(ch1, p))
                continue
            if tp1 in (2, 4):
                continue
            if tp1 == tp2:
                self.tokens[-1].token += ch1
            else:
                self.tokens.append(Token(ch1, p))
                if tp1 == 0:
                    self.tokens[-1].word = True
                if tp1 == 1:
                    self.tokens[-1].val = True
                if tp1 == 3:
                    self.tokens[-1].op = True

    def fix_tokens(self):
        # Fix operator symbols
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.op:
                self.tokens.pop(i)
                all_chars = token.token
                while all_chars != "":
                    for pref_len in range(self.procedure.config.mx_op_size, 0, -1):
                        prefix = all_chars[:pref_len]
                        simp, rev = self.is_finished_operator(prefix)
                        if simp:
                            self.tokens.insert(i, Token(prefix, op=True))
                            i += 1
                            all_chars = all_chars[pref_len:]
                            break
                    else:
                        raise Exception("Illegal char sequence, started at %d: %s" % (token.st + 1, token.token))
            i += 1
        # Fix points
        # TODO: remove crutches
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.token == ".":
                length = 1
                res = [""] * 2
                mn = i
                for j in range(1, -1, -1):
                    k = j * 2 - 1
                    if 0 <= i + k < len(self.tokens) and self.tokens[i + k].val:
                        res[j] = self.tokens[i + k].token
                        mn = i + k
                        length += 1
                if res != [""] * 2:
                    for j in range(length):
                        self.tokens.pop(mn)
                    self.tokens.insert(mn, Token(".".join(res), val=True))
            i += 1

    def __call__(self):
        self.split_to_tokens()
        self.fix_tokens()
        self.procedure.tokens = self.tokens
