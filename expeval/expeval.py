from queue import Queue
from typing import List, Tuple
from expeval.expeval_std import std_names, std_specific_operators, CharOperator, Namespace
from lib.killable_thread import KillableThread


# TODO: fix counting token place everywhere
# TODO: add classes like WordToken, OperatorToken etc...
class Token:
    def __init__(self, token, st=-1, word=False, val=False, op=False):
        """
        Crutch
        -1 means that it doesn't mater
        """
        self.token = token
        self.st = st
        self.word = word
        self.val = val
        self.op = op

class CalculationTimeoutExpired(Exception):
    pass


class ExpEval:
    names: Namespace
    specific_operators: List[CharOperator]

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
        self.pares = {"<": ">", "\\": "/"}
        self.brackets = {"(": "),", "[": "]", "{": "}"}

        # execution levels
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

    def comp_exp(self, query) -> Tuple[str, str, bool]:
        try:
            q = Queue()
            thread = KillableThread(target=lambda config, query, queue: queue.put(ExpEvalProcedure(config, query)()), args=(self, query, q))
            thread.start()
            thread.join(1)
            if thread.is_alive():
                thread.kill()
                raise CalculationTimeoutExpired()
            return q.get()
        except Exception as err:
            return str(err), "", False


class ExpEvalProcedure:
    def __init__(self, config: ExpEval, query):
        self.config = config
        self.query = query

    def __call__(self):
        tokenizer = Tokenizer(self, self.query)
        tokens = tokenizer()
        executor = Executor(self, tokens)
        return executor()


from expeval.tokenizer import Tokenizer
from expeval.executor import Executor
