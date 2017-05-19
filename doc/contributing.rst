Contributing
============

**First:** Fork, then clone the repo:

    git clone git@github.com:your-username/flagon.git

Guidelines
----------
Please conform to the
`pep8 <https://www.python.org/dev/peps/pep-0008/>`_) specifica8tion for
code formatting.


Write `unittests <https://github.com/ashcrow/flagon/tree/master/test>`_
for any new functionality, if you are up to the task. Not a
requirement, but is does get you a lot of karma.


Write
`intelligent commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_.


Hacking
=======

Build the RPM
-------------

.. code-block:: bash

    $ make rpm
    ... lots of output here ...

    #############################################
    python-flagon RPMs are built:
    rpm-build/python-flagon-0.0.1-1.fc20.src.rpm
    rpm-build/noarch/python-flagon-0.0.1-1.fc20.noarch.rpm
    #############################################


Updating the RPM Spec/Python setup.py files
===========================================

.. note::

  When updating `the RPM spec file <https://github.com/ashcrow/flagon/blob/master/contrib/rpm/python-flagon.spec.in>`_, be sure you update the ``.in`` file. The same rule applies to updating the `the Python setup.py file <https://github.com/ashcrow/flagon/blob/master/setup.py.in>`_.

Remember that the **Version** while building the software is
controlled by the contents of the
`VERSION <https://github.com/ashcrow/flagon/blob/master/VERSION>`_ file.
