from typing import List, Tuple
from .expeval import ExpEvalProcedure, Token
from .ulib.useful import is_from_same


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
        return (ord("a") <= ord(char.lower()) <= ord("z")) or char == "_"

    @staticmethod
    def is_digit(char: str):
        return ord("0") <= ord(char) <= ord("9")

    def decide_operator_orientation(self, _operator: str) -> Tuple[str, bool]:
        op = list(_operator)
        rev = False
        rev_decided = False
        for i in range(len(op)):
            ch = op[i]
            if ch in self.procedure.config.pares:
                if rev_decided and not rev:
                    return "", False  # Failure
                rev, rev_decided = True, True
                op[i] = self.procedure.config.pares[ch]
            elif ch in self.procedure.config.pares.values():
                if rev_decided and rev:
                    return "", False
                rev, rev_decided = False, True
        return "".join(op), rev

    def simplify_single_operator(self, operator: str) -> Tuple[str, bool, str]:
        no_rev_operator, rev = self.decide_operator_orientation(operator)
        return no_rev_operator, rev, "".join(sorted(no_rev_operator))

    def is_finished_single_operator(self, my_op) -> Tuple[str, bool]:
        faze_one, rev, faze_two = self.simplify_single_operator(my_op)
        if not faze_one:
            return "", False
        for op in self.procedure.config.specific_operators:
            if (self.procedure.config.specific_operators[op].allow_shuffle and\
                    self.simplify_single_operator(op)[2] == faze_two) or op == faze_one:
                return op, rev
        return "", False

    def get_single_char_op_sides(self, in_br_op):
        return self.procedure.config.names[self.procedure.config.specific_operators[in_br_op[0]].replace].sides

    def is_finished_operator(self, my_op) -> List[Tuple[str, bool]]:
        res = []
        while my_op != "":
            for pref_len in range(self.procedure.config.mx_op_size, 0, -1):
                prefix = my_op[:pref_len]
                op, rev = self.is_finished_single_operator(prefix)
                if op:
                    res.append((op, rev))
                    my_op = my_op[pref_len:]
                    break
            else:
                return []
        same_sides = is_from_same(map(self.get_single_char_op_sides, res))
        return res if same_sides else []

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
            if tp1 == tp2 or (tp1, tp2) == (1, 0):
                self.tokens[-1].token += ch1
            else:
                self.tokens.append(Token(ch1, p))
                if tp1 == 0:
                    self.tokens[-1].word = True
                if tp1 == 1:
                    self.tokens[-1].val = True
                if tp1 == 3:
                    self.tokens[-1].op = True

    def __call__(self):
        self.split_to_tokens()
        tokenizer_fixer = TokenizerFixer(self)
        self.tokens = tokenizer_fixer()
        return self.tokens


from .tokenizer_fixer import TokenizerFixer
