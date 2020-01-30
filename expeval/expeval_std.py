import math
from typing import Tuple, Callable, List
from .ulib.useful import UsefulObj


class ExitSignal(Exception):
    """
If you want to exit testing shell, you should write operator exit.
It will send ExitSignal and exit from testing shell
    """


class Operator(UsefulObj):
    level: int
    sides: Tuple[bool, bool, bool]
    func: Callable


class CompSingCopyOperator(Operator):
    def __init__(self, op: Operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_from_parent(op, ("level", "sides", "func"))

    rev: bool = False
    from_heaven = []


class CharOperator(UsefulObj):
    replace: str
    allow_shuffle = False
    from_heaven = []
    branching = True


class CompOperator(UsefulObj):
    branches: List[CompSingCopyOperator]
    args_trick = ["branches"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = self.branches[0]

    def get_level(self):
        return min(map(lambda op: op.level, self.branches))


class Namespace(UsefulObj):
    cont: dict

    def apply_path(self, path: str):
        sp_res = path.split(".", 1)
        in_me = self.cont[sp_res[0]]
        if len(sp_res) == 1:
            return in_me
        return in_me.apply_path(sp_res[1])

    @staticmethod
    def try_std_op_to_this(maybe_op):
        if isinstance(maybe_op, Operator):
            return CompOperator(branches=[CompSingCopyOperator(maybe_op)])
        else:
            return maybe_op

    def __iter__(self):
        return self.cont.__iter__()

    def __getitem__(self, item: str):
        return self.apply_path(item)


def cnpk(n, k):
    res = 1
    for u in range(n, n - k, -1):
        res *= u
    res //= math.factorial(k)
    return res


def exgcd(a, b):
    if b == 0:
        return 1, 0, a
    y, x, gcd = exgcd(b, a % b)
    return x, y - (a // b) * x, gcd


def send_exit_signal_to_testing_shell():
    raise ExitSignal("exiting from testing shell")


# TODO: isolate names and word_operators like were isolated names and char operators
std_names = Namespace(cont={
    "comb": Namespace(cont={
        "comb_c": cnpk
    }),
    "pi": math.pi,
    "__addition__": Operator(level=1, sides=(True, False, True), func=lambda a, b, c: a + b * c),
    "__fact__": Operator(level=3, sides=(True, False, False), func=math.factorial),
    "mod": Operator(level=1, sides=(True, True, True), func=lambda a, bl, c: a % bl[0] == c % bl[0]),
    "sqrt": math.sqrt,
    "__multiplication__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a * b),
    "__division__": Operator(level=2, sides=(True, False, True), func=lambda a, b: a / b),
    "exit": Operator(level=0, sides=(False, False, False), func=send_exit_signal_to_testing_shell)
})

std_specific_operators = {
    "+": CharOperator(replace="__addition__", from_heaven=[1]),
    "-": CharOperator(replace="__addition__", from_heaven=[-1]),
    "!": CharOperator(replace="__fact__", branching=False),
    "*": CharOperator(replace="__multiplication__"),
    "/": CharOperator(replace="__division__")
}
