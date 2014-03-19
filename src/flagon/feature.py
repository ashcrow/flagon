import logging

from functools import wraps

from flagon import errors


def create_decorator(backend, logger):
    """
    Creates a decorator using the given backend and logger.
    """

    logger.debug(
        'The feature decorator for flagon has been created with %s' % (
        backend.__class__.__name__))

    def feature(name, default=None):
        if not backend.exists(name):
            logger.error('An unknown feature was requested: %s' % name)
            raise errors.UnknownFeatureError('Unknown feature: %s' % name)

        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if backend.is_on(name):
                    return func(*args, **kwargs)
                if default:
                    logger.warn(
                        'Disabled featured %s was requested.'
                        ' Using default.' % name)
                    if logging.getLevelName(logger.level) == 'DEBUG':
                        import inspect
                        logger.debug('%s default=%s:%s(*%s, **%s)' % (
                            name, inspect.getabsfile(default),
                            default.__name__, args, kwargs))
                    return default(*args, **kwargs)
                else:
                    logger.warn('Disabled featured %s was requested' % name)
                raise NameError("name '%s' is not enabled" % name)
            return wrapper
        return deco
    return feature


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
    feature = create_decorator(backend, logger)
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
