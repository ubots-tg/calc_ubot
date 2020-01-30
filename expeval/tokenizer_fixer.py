from typing import List
from .expeval import Token
from .tokenizer import Tokenizer


class TokenizerFixer:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.tokens: List[Token] = tokenizer.tokens
        self.i = 0

    def fix_stuck_operator(self):
        token = self.tokens[self.i]
        self.tokens.pop(self.i)
        all_chars = token.token
        while all_chars != "":
            for pref_len in range(len(all_chars), 0, -1):
                prefix = all_chars[:pref_len]
                branches = self.tokenizer.is_finished_operator(prefix)
                if branches:
                    self.tokens.insert(self.i, Token(branches, op=True))
                    self.i += 1
                    all_chars = all_chars[pref_len:]
                    break
            else:
                raise Exception("Illegal char sequence, started at %d: %s" % (token.st + 1, token.token))
        self.i -= 1

    def fix_dot_token(self):
        length = 1
        res = [""] * 2
        mn = self.i
        for j in range(2):
            k = j * 2 - 1
            if 0 <= self.i + k < len(self.tokens) and self.tokens[self.i + k].val:
                res[j] = self.tokens[self.i + k].token
                mn = min(mn, self.i + k)
                length += 1
        if res != [""] * 2:
            for j in range(length):
                self.tokens.pop(mn)
            self.tokens.insert(mn, Token(".".join(res), val=True))
            self.i = mn

    def __call__(self,):
        while self.i < len(self.tokens):
            if self.tokens[self.i].op:
                self.fix_stuck_operator()
            elif self.tokens[self.i].token == ".":
                self.fix_dot_token()
            self.i += 1
        return self.tokens
