from logging import Logger
import sys
import importlib

from . import get_logger

logger = get_logger()

class Reload():
    def __call__(self, name):
        if isinstance(name, str):
            name = [name]

        reloaded = False
        to_reload = set(name)
        for mod_name, mod in sys.modules.items():
            if mod_name in to_reload:
                importlib.reload(mod)
                logger.info("%s", f"Mod reloaded: {mod_name}")
                reloaded = True

        if not reloaded:
            logger.info("%s", "No modules to reload")

reload = Reload()
