from typing import List
from expeval.expeval import ExpEvalProcedure, Token


# class UbotRatioInt:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def __float__(self):
#         return self.a / self.b


# class InBrackets:
#     def __init__(self, config):
#         self.open, self.sep, self.close = config

class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens: List[Token]):
        self.procedure = procedure
        self.tokens = tokens.copy()

    def simplify_br_set_func(self, left):
        """brackets -> sets -> functions"""
        right = left + 1
        while True:
            token = self.tokens[right]
            if isinstance(token, Token):
                if token.token == "(":
                    pass
                elif token.token == ")":
                    pass
            right += 1

    def __call__(self):
        self.tokens.insert(0, Token("("))
        self.tokens.append(Token(")"))
        # TODO: сделать что-то
        return self.tokens[0], ""


from expeval.expeval_funcs import exgcd
