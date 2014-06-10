Usage
=====

Backends
--------
First thing to do is to choose a backend to use. A backend


Crating the feature instance
----------------------------
When creating a feature instance one must pass a backend and an optional logger to use.

.. code-block:: python

   from flagon import Feature
   from flagon.backends.jsonfile import JSONFileBackend
   # Make a backend
   backend = JSONFileBackend('example/config.json')
   # Make the feature instance
   feature = Feature(backend)


Using the feature instance
--------------------------
Once a feature instance has been made it then can be used to tag callables as features. To do this one uses the feature instance as a decorator.

.. code-block:: python

   @feature('a feature')
   def say_something(data):
       print data

Now that the function ``say_something`` has been tagged with the feature ``a feature`` it will only execute if ``a feature`` is set active.

.. note::

   When features are not active they will raise a NameError unless there is a default set.

.. note::

   When a feature is unknown it will raise an flagon.errors.UnknownFeatureError


Defaults
~~~~~~~~
Feature instance can also define defaults. Defaults are callables that will call **instead** of the original callable if the feature is off.

.. code-block:: python

   def yell(data):
       print data.upper()

   @feature('this feature is off', default=yell)
   def say_something(data):
       print data
