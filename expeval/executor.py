from typing import List, Tuple
from expeval.expeval import ExpEvalProcedure, Token
from expeval.expeval_std import Namespace, Operator, CompOperator


class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens):
        self.procedure = procedure
        self.env: List = tokens.copy()

    def is_for_call(self, p):
        before = self.env[p - 1]
        return callable(before) or isinstance(before, CompOperator)

    def brackets(self, sti, bracket, belong_as_tuple):
        p = sti + 1
        end_bracket = self.procedure.config.brackets[bracket]
        while True:
            if isinstance(self.env[p], Token):
                tk: Token = self.env[p]
                if tk.token == end_bracket:
                    eni = p
                    break
                elif tk.token in self.procedure.config.brackets:
                    self.brackets(p, tk.token, False)
                elif tk.op:
                    br = self.env.pop(p).token
                    transformed: List[Operator] = []
                    for op_path, rev in br:
                        transformed.append(self.procedure.config.names[op_path])
                        transformed[-1].rev = rev
                    self.env.insert(p, CompOperator(transformed))
                elif tk.word:
                    from_root_val = self.procedure.config.names[self.env.pop(p).token]
                    self.env.insert(p, from_root_val)
                elif tk.token == ".":
                    # At this place, point is using only to use "namespaces".
                    ns = self.env[p - 1]
                    wrd_tok = self.env[p + 1]
                    if not(isinstance(ns, Namespace) and wrd_tok.word):
                        raise Exception("Point that doesn't binds namespace and link at place % d" % tk.st)
                    next_val = ns[wrd_tok.tok]
                    self.env[p - 1] = next_val
                    self.env.pop(p)
                    self.env.pop(p + 1)
                    p -= 1
            p += 1

    def __call__(self):
        self.env.insert(0, Token("("))
        self.env.append(Token(")"))
        self.brackets(0, "(", False)
        return self.env[0], ""
