
import unittest


def make_logger():
    import logging
    logger = logging.getLogger('flagon')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(name)s - %(levelname)s - %(msg)s'))
    logger.handlers.append(handler)
    logger.setLevel(logging.CRITICAL)
    return logger


class TestCase(unittest.TestCase):
    pass
