from typing import List, Tuple
from expeval.expeval import ExpEvalProcedure, Token
from expeval.expeval_std import Namespace, Operator, CompOperator


class Executor:
    def __init__(self, procedure: ExpEvalProcedure, tokens):
        self.procedure = procedure
        self.env: List = tokens.copy()

    def replace_range(self, start, length, value):
        cleaning_progress = 0
        while cleaning_progress < length:
            self.env.pop(start)
            cleaning_progress += 1
        self.env.insert(start, value)

    @staticmethod
    def execute_single_operator(single_operator: Operator, left_n_right, dop):
        if single_operator.rev:
            left_n_right = left_n_right[::-1]
        op_func_result = single_operator.func(*(left_n_right + dop + single_operator.from_heaven))
        return op_func_result

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
            self.replace_range(sti, 2 * len(_tuple) + 1, _tuple)
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
                    elif tk.token == "(":
                        # Bracket for functions
                        called_by_func = callable(self.env[p - 1])
                        called_by_operator = isinstance(self.env[p - 1], CompOperator)
                        self.brackets(p, tk.token, 1 if called_by_func or called_by_operator else 0)
                        if called_by_func:
                            p -= 1
                            func_res = self.env[p](self.env[p + 1])
                            self.replace_range(p, 2, func_res)
                    elif tk.token in self.procedure.config.brackets:
                        # Other brackets
                        self.brackets(p, tk.token, 1)
                    elif tk.op:
                        br = self.env.pop(p).token
                        transformed: List[Operator] = []
                        for op_path, rev in br:
                            char_op = self.procedure.config.specific_operators[op_path]
                            transformed.append(self.procedure.config.names[char_op.replace])
                            transformed[-1].rev = rev
                            transformed[-1].from_heaven = char_op.from_heaven
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
                p = sti + 1
                while True:
                    if isinstance(self.env[p], Token):
                        if self.env[p].token in (end_bracket, self.procedure.config.sep):
                            break
                    elif isinstance(self.env[p], CompOperator):
                        operator: CompOperator = self.env[p]
                        if operator.get_level() == cur_level:
                            # left, right, dop, from_heaven
                            dop_information = left_n_right = []
                            if operator.model.sides[1]:
                                # Нам не мешает никак
                                dop_information = self.env.pop(p + 1)
                            if operator.model.sides[0]:
                                left_n_right.append(self.env.pop(p - 1))
                                p -= 1
                            if operator.model.sides[2]:
                                left_n_right.append(self.env.pop(p + 1))

                            if operator.branches.__len__() == 1:
                                op_res = self.execute_single_operator(operator.model,
                                                                      left_n_right.copy(), dop_information)
                            else:
                                op_res = set()
                                for single_operator in operator.branches:
                                    op_res.add(self.execute_single_operator(single_operator,
                                                                            left_n_right.copy(), dop_information))
                            # TODO: replace operator construction by result

            res = self.env[sti + 1]
            if mode == 1:
                self.replace_range(sti, 3, res)
            else:
                return res

    def __call__(self):
        self.env.insert(0, Token("("))
        self.env.append(Token(")"))
        self.brackets(0, "(", False)
        return self.env[0], ""
