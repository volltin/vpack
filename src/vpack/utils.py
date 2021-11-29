import logging

# logging.basicConfig()
logger = logging.getLogger("vpack")
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('(%(name)s): %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

def get_logger():
    return logger
