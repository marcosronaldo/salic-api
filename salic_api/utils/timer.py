import logging
import time
from contextlib import contextmanager

log = logging.getLogger('salic-api')


@contextmanager
def timer(action, verbose=True):
    """
    Log results for the time required to execute the given action.

    Used as a context manager:
    >>> with timer('foo'):
    ...     print('hello world!')
    """

    start = time.time()
    if verbose:
        log.debug('Start action: %r' % action)
    try:
        yield
    finally:
        msecs = (time.time() - start) * 1000
        if verbose:
            log.debug('Action completed in %f ms' % msecs)
