from colorama import Fore
import time
from . import ExpEval, ExpEvalProcedure
from .ulib import Signal


if __name__ == '__main__':
    ex = ExpEval()
    while True:
        query = input(Fore.CYAN + "> " + Fore.RESET)
        try:
            time_start = time.time()
            result, pretty_result = ExpEvalProcedure(ex, query)()
            time_ready = time.time()
            print(f"{Fore.YELLOW}%s{Fore.RESET}={Fore.GREEN}%s{Fore.RESET}={Fore.MAGENTA}%s{Fore.RESET}" % (query, result, pretty_result))
            print("It took %d seconds to execute" % (time_ready - time_start))
        except Exception as err:
            if isinstance(err, Signal):
                err: Signal
                if err.name == "exit":
                    break
            else:
                print(Fore.RED, end="")
                print("Oh no! %s!" % err.__class__.__name__)
                print(err)
                print(Fore.RESET, end="")
else:
    print("Ты паровозик?")
