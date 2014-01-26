flagon
======

Feature flags for python.

**Note**: This is mainly experimenting to find the best method for Python feature flagging.

Example
-------
(Run python src/flagon/feature.py to see results)

``python
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
```
