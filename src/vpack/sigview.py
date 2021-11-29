import os
import signal
import inspect

from colorama import Fore, Back, Style
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer

class Sigview:
    def __init__(self) -> None:
        self.lexer = Py3Lexer(ensurenl=False)
        self.formatter = Terminal256Formatter()

    def display_frame(self, frame):
        frameinfo = inspect.getframeinfo(frame)
        filename = frameinfo.filename
        lineno = frameinfo.lineno
        function = frameinfo.function
        code_context = frameinfo.code_context
        text = '{}:{} in {}'.format(filename, lineno, function)
        code = highlight(code_context[0], self.lexer, self.formatter)
        print(Fore.CYAN + "===  Sigview  ===" + Style.RESET_ALL)
        print(Fore.CYAN + text + Style.RESET_ALL)
        print(code)
        print(Fore.CYAN + "=== /Sigview  ===" + Style.RESET_ALL)

    def sigview_handler(self, signum, frame):
        self.display_frame(frame)

    def enable(self,
        signum=signal.SIGUSR1,
        pidfile="/tmp/.sigview.pid",
        cmdfile="/tmp/.sigview.cmd",
        ):
        pid = os.getpid()
        if pidfile is not None:
            with open(pidfile, "w") as f:
                f.write("{pid}")
        if cmdfile is not None:
            with open(cmdfile, "w") as f:
                f.write(f"kill -s SIGUSR1 {pid}")
        print(f"sigview enabled. pid={pid}, saved pid to {pidfile}, cmd tp {cmdfile}")
        signal.signal(signum, self.sigview_handler)

sigview = Sigview()
