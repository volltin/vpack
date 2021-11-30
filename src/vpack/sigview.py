import os
import pdb
import time
import signal
import inspect
import textwrap
import traceback

from colorama import Fore, Back, Style
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer

from . import get_logger

logger = get_logger()

class Sigview:
    last_time_pressed = 0.0
    interval = 0.5
    openshell = False

    def __init__(self) -> None:
        self.lexer = Py3Lexer(ensurenl=False)
        self.formatter = Terminal256Formatter(style='friendly')

    def bordered(self, text):
        lines = text.splitlines()
        width = max(len(s) for s in lines)
        header = ['+-' + '-' * width + '-+']
        footer = ['+-' + '-' * width + '-+']
        leading = '| '
        trailing = ' |'
        return '\n'.join(header + [leading + s.ljust(width) + trailing for s in lines] + footer)

    def display_frame(self, frame):
        try:
            frameinfo = inspect.getframeinfo(frame)
            filename = frameinfo.filename
            lineno = frameinfo.lineno
            function = frameinfo.function
            code_context = frameinfo.code_context
            text = '{}:{} in {}'.format(filename, lineno, function)
            logger.info("Current file:\n%s", Fore.CYAN + text + Style.RESET_ALL)

            stacktext = '\n'.join(traceback.format_stack(f=frame))
            stacktext = textwrap.dedent(stacktext)
            stacktext = self.bordered(stacktext)
            stacktext = highlight(stacktext, self.lexer, self.formatter)

            logger.info("Current stask:\n%s", stacktext)
        except Exception as e:
            logger.exception(e)

    def try_openshell(self, frame):
        if self.openshell:
            pdb.Pdb().set_trace(frame)

    def enable_openshell(self):
        self.openshell = True

    def disable_openshell(self):
        self.openshell = False

    def sigview_once_handler(self, signum, frame):
        self.display_frame(frame)
        self.try_openshell(frame)


    def sigview_twice_handler(self, signum, frame):
        t_now = time.time()
        t_pre = self.last_time_pressed
        if t_now - t_pre > self.interval:
            self.display_frame(frame)
            self.try_openshell(frame)
        else:
            raise KeyboardInterrupt
        self.last_time_pressed = time.time()

    def enable_once(self,
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
        logger.info("%s", f"sigview enabled. pid={pid}, saved pid to {pidfile}, cmd to {cmdfile}")
        signal.signal(signum, self.sigview_once_handler)

    def enable_twice(self, signum=signal.SIGINT):
        logger.info("%s", f"Sigview enabled. Press ^C to see the current frame. Press ^C again to exit.")
        signal.signal(signum, self.sigview_twice_handler)

    def enable(self, mode='twice', openshell=False):
        self.openshell = openshell
        if mode == 'once':
            self.enable_once()
        elif mode == 'twice':
            self.enable_twice()
        else:
            raise ValueError(f"unknown mode: {mode}")

sigview = Sigview()
