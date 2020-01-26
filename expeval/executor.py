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

    def brackets(self, sti, bracket, mode):
        """
        :param sti:
        :param bracket:
        :param mode:
        0 - prosto skobki
        1 - called
        2 - (,  or  ,,  or  ,)
        :return: something if mode = 2 and nothing in other case
        """
        end_bracket = self.procedure.config.brackets[bracket]
        if mode == 1:
            p = sti
            _tuple = []
            while True:
                elem = self.brackets(sti, bracket, 2)
                _tuple.append(elem)
                if self.env[p].token == end_bracket:
                    break
                p += 2
            for cleaning_progress in range(2 * len(_tuple) + 1):
                self.env.pop(sti)
            self.env.insert(sti, _tuple)
        else:
            p = sti + 1
            while True:
                if isinstance(self.env[p], Token):
                    tk: Token = self.env[p]
                    if tk.token == end_bracket:
                        break
                    if tk.token == self.procedure.config.sep:
                        if mode == 3:
                            break
                        else:
                            raise Exception("Are you stupid? Wtf a separator doing here (%d)" % tk.st)
                    elif tk.token in self.procedure.config.brackets:
                        self.brackets(p, tk.token, 1 if self.is_for_call(p) else 0)
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
            for cur_level in self.procedure.config.execution_levels:
                pass

    def __call__(self):
        self.env.insert(0, Token("("))
        self.env.append(Token(")"))
        self.brackets(0, "(", False)
        return self.env[0], ""
