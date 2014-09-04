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
