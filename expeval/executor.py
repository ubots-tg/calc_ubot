from typing import List
from expeval.expeval import ExpEvalProcedure, Token


# class InBrackets:
#     def __init__(self, config):
#         self.open, self.sep, self.close = config

class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens):
        self.procedure = procedure
        self.env = tokens.copy()

    def brackets(self, sti, bracket, belong_as_tuple):
        end_bracket = self.procedure.config.brackets[bracket]

    # def simplify_br_set_func(self, left):
    #     """brackets -> sets -> functions"""
    #     right = left + 1
    #     while True:
    #         token = self.env[right]
    #         if isinstance(token, Token):
    #             if token.token == "(":
    #                 pass
    #             elif token.token == ")":
    #                 pass
    #         right += 1

    def __call__(self):
        self.env.insert(0, Token("("))
        self.env.append(Token(")"))
        # TODO: сделать что-то
        return self.env[0], ""


from expeval.expeval_funcs import exgcd
