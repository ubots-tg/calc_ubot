from typing import List
from expeval.expeval import ExpEvalProcedure, Token


class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens: List[Token]):
        self.procedure = procedure
        self.tokens = tokens

    def execute_token_sequence_inside_brackets(self, left):
        pass

    def __call__(self):
        self.tokens.insert(0, Token("("))
        self.tokens.append(Token(")"))
        self.execute_token_sequence_inside_brackets(0)
        # TODO: сделать что-то
        return self.tokens[0], ""
