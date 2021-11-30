import sys
import types
import inspect
import traceback, pdb
from colorama import Fore, Back, Style

from . import get_logger

logger = get_logger()

class Breakpt:
    _cnt = {}
    _enable = True

    def __init__(self) -> None:
        self._enable = True

    def enable(self):
        self._enable = True

    def disable(self):
        self._enable = False

    def auto(self):
        self._enable = hasattr(sys, "ps1") or not sys.stderr.isatty()

    def break_fn(self):
        """
        make sure this function (`break_fn`) is called with depth=2:
            user_fn() -> some_internal_fn() -> break_fn()
        """
        if not self._enable:
            return

        try:
            from IPython import embed

            """
            Dirty hack for IPython.embed():
                frame = sys._getframe(1)
                shell(header=header, stack_depth=2, compile_flags=compile_flags, ...)

            replace consts `1` and `2` with `3` and `4`.
            """

            new_consts = list(embed.__code__.co_consts)
            for i, c in enumerate(new_consts):
                if isinstance(c, int) and c == 1:
                    new_consts[i] = 3
                if isinstance(c, int) and c == 2:
                    new_consts[i] = 4

            new_consts = tuple(new_consts)

            x = embed.__code__
            if sys.version_info >= (3, 8):
                # co_posonlyargcount is new in Python 3.8
                __new_code__ = types.CodeType(
                    x.co_argcount, x.co_posonlyargcount, x.co_kwonlyargcount, x.co_nlocals, x.co_stacksize,
                    x.co_flags, x.co_code, new_consts, x.co_names, x.co_varnames, x.co_filename, x.co_name,
                    x.co_firstlineno, x.co_lnotab, x.co_freevars, x.co_cellvars
                )
            else:
                __new_code__ = types.CodeType(
                    x.co_argcount, x.co_kwonlyargcount, x.co_nlocals, x.co_stacksize, x.co_flags,
                    x.co_code, new_consts, x.co_names, x.co_varnames, x.co_filename, x.co_name,
                    x.co_firstlineno, x.co_lnotab, x.co_freevars, x.co_cellvars
                )

            embed.__code__ = __new_code__
            embed(colors="neutral")
            embed.__code__ = x
        except ImportError:
            logger.info(Fore.RED + "No IPython installed, using pdb insdead. Strongly recommend to install IPython." + Style.RESET_ALL)
            from pdb import Pdb
            user_frame = sys._getframe(2)
            Pdb().set_trace(user_frame)

    def at(self, times):
        """
        break at `times` times
        """

        call_frame = inspect.currentframe().f_back
        call_frame_info = inspect.getframeinfo(call_frame)
        cnt_key = call_frame_info.filename + ":" + str(call_frame_info.lineno)
        if cnt_key not in self._cnt:
            self._cnt[cnt_key] = 0
        self._cnt[cnt_key] += 1
        if self._cnt[cnt_key] == times:
            logger.info(Fore.CYAN + "Breakpoint hit (called %d times from this line)" + Style.RESET_ALL, times)
            self.break_fn()

    def always(self):
        self.break_fn()

    def onerror(self):
        def excepthook(type, value, tb):
            if not self._enable:
                sys.__excepthook__(type, value, tb)
                return
            traceback.print_exception(type, value, tb)
            pdb.post_mortem(tb)

        sys.excepthook = excepthook

breakpt = Breakpt()





