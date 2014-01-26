
from functools import wraps

from flagon import errors

from flagon.backends.jsonfile import JSONFileBackend


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
                logger.warn('Disabled featured %s was requested' % name)
                if default:
                    return default(*args, **kwargs)
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

    # Make a backend
    backend = JSONFileBackend('example/config.json')

    # Make the decorator
    feature = create_decorator(backend, logger)

    @feature('test')
    def t(a):
        print a

    print "\n* Executing feature 'test' with 'asd': "
    t('asd')

    @feature('off')
    def o(a):
        print a

    print "\n* Executing feature 'off' (which is turned off) with 'asd'"
    try:
        o('asd')
    except NameError, ne:
        print type(ne), ne

    print "\n* Defining 'doesnotexist' (which is not a configured feature)"
    try:
        @feature('doesntexist')
        def d(a):
            print a
    except errors.UnknownFeatureError, ufe:
        print type(ufe), ufe
