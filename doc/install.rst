Installation
============

pip
---
Flagon can be installed via the normal pip command syntax.

.. code-block:: bash

   $ pip install flagon


source
------
Flagon can be installed via ``setup.py`` in the source directory:

.. code-block:: bash

   $ python setup.py install


rpm
---
For RPM based systems an RPM can be generated.

.. code-block:: bash

   $ make rpm
   ....
   $ sudo rpm -ivh rpm-build/noarch/flaggon*rpm
