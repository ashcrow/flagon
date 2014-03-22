import inspect
import logging

from functools import wraps

from flagon import errors


class Feature(object):
    """
    The feature manager.
    """

    def __init__(self, backend, logger):
        """
        Creates the feature manager.

        backend is the backend to use for storing feature states.
        logger is the logger like object to use for logging.
        """
        self.backend = backend
        self.logger = logger
        self.logger.debug(
            'The feature decorator for flagon has been created with %s' % (
            backend.__class__.__name__))

    def __call__(self, name, default=None):
        """
        What acts as a decorator.

        name is the name of the feature.
        default is the default callable to fall back to.
        """
        if not self.backend.exists(name):
            self.logger.error('An unknown feature was requested: %s' % name)
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self.backend.is_active(name):
                    self.logger.debug('%s func=%s:%s(*%s, **%s)' % (
                        name, inspect.getabsfile(func),
                        func.__name__, args, kwargs))
                    return func(*args, **kwargs)
                if default:
                    self.logger.warn(
                        'Disabled featured %s was requested.'
                        ' Using default.' % name)
                    if logging.getLevelName(self.logger.level) == 'DEBUG':
                        self.logger.debug('%s default=%s:%s(*%s, **%s)' % (
                            name, inspect.getabsfile(default),
                            default.__name__, args, kwargs))
                    return default(*args, **kwargs)
                else:
                    self.logger.warn('Disabled featured %s was requested' % (
                        name))
                raise NameError("name '%s' is not enabled" % name)
            return wrapper
        return deco

    is_active = lambda s, name: s.backend.is_active(name)


if __name__ == '__main__':
    # Example

    # Make a logger
    import logging
    logger = logging.getLogger('flagon')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(name)s - %(levelname)s - %(msg)s'))
    logger.handlers.append(handler)
    logger.setLevel(logging.DEBUG)

    # --- FLAGON SPECIFIC CODE ---
    from flagon.backends.jsonfile import JSONFileBackend
    # Make a backend
    backend = JSONFileBackend('example/config.json')

    # Make the decorator
    feature = Feature(backend, logger)
    # --- END FLAGON SPECIFIC CODE---

    # Now to use flagon for feature flagging

    @feature('test')
    def t(a):
        print "FROM t()", a

    print "\n* Executing feature 'test' with 'asd': "
    t('asd')

    @feature('off')
    def o(a):
        print "FROM a()", a

    @feature('withdefault', default=t)
    def v(a):
        print "FROM v()", a

    print "\n* Executing feature 'off' (which is turned off) with 'asd'"
    try:
        o('asd')
    except NameError, ne:
        print type(ne), ne

    print (
        "\n* Executing feature 'withdefault' (which is turned off) "
        "which passed a default implementation of the t function.")
    v('asd')

    print "\n* Defining 'doesnotexist' (which is not a configured feature)"
    try:
        @feature('doesntexist')
        def d(a):
            print a
    except errors.UnknownFeatureError, ufe:
        print type(ufe), ufe
