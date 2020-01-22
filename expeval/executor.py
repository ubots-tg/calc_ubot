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
        p = sti
        end_bracket = self.procedure.config.brackets[bracket]
        while True:
            if isinstance(self.env[p], Token):
                tk: Token = self.env[p]
                if tk.token == end_bracket:
                    eni = p
                    break
                elif tk.token in self.procedure.config.brackets:
                    self.brackets(p, tk.token, False)
                elif tk.token == ".":
                    # At this place, point is using only to use "namespaces".
                    path_word = []
                    for j in (-1, 1):
                        if sti < p + j < len(self.env) and self.env[p + j].word:
                            path_word.append(self.env[p + j].token)
                        else:
                            raise Exception("Point that doesn't binds namespace and link at place % d" % tk.st)
            p += 1

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
        self.brackets(0, "(", False)
        return self.env[0], ""
