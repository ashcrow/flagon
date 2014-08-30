flagon
======
[![Build Status](https://api.travis-ci.org/ashcrow/flagon.png)](https://travis-ci.org/ashcrow/flagon/)


Generic feature flags for python which attempts to be compatible with
Java's Togglz (http://www.togglz.org/).

Ideas
-----
* Pluggable configuration backends
* Support for default fallback calls
* Logging support


Example
-------
* Code: https://github.com/ashcrow/flagon/blob/master/example/example.py
* Config: https://github.com/ashcrow/flagon/blob/master/example/config.json
* Results: https://github.com/ashcrow/flagon/blob/master/example/results.txt
* Django Example: https://github.com/ashcrow/flagon/tree/master/example/djproject

Status API
----------
a simple flag status api is provided under flagon.status_api. Example wsgi file can be found in contrib/wsgi. The status api requires [werkzeug](http://werkzeug.pocoo.org).


The request endpoint is /v0/*FLAG_NAME*.

The response syntax is JSON format with two keys with bools: active, known.

* active is if the flag is on or not.
* known is noting if the flag exists.
