flagon
======

Feature flags for python.

**Note**: This is mainly experimenting to find the best method for Python feature flagging.


Ideas
-----
* Pluggable configuration backends
* Support for default fallback calls
* Logging support


Example
-------
Configuration file: https://github.com/ashcrow/flagon/blob/master/example/config.json


```python
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
# Make a backend
backend = JSONFileBackend('example/config.json')

# Make the decorator
feature = create_decorator(backend, logger)
# --- END FLAGON SPECIFIC CODE---

# Now to use flagon for feature flagging

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

Example Results
---------------

```
warnings.warn('JSONFileBackend is not safe for multi-write environments')
flagon - DEBUG - The feature decorator for flagon has been created with JSONFileBackend

* Executing feature 'test' with 'asd':
asd

* Executing feature 'off' (which is turned off) with 'asd'
flagon - WARNING - Disabled featured off was requested
<type 'exceptions.NameError'> name 'off' is not enabled

* Defining 'doesnotexist' (which is not a configured feature)
flagon - ERROR - An unknown feature was requested: doesntexist
<class 'flagon.errors.UnknownFeatureError'> Unknown feature: doesntexist
```
