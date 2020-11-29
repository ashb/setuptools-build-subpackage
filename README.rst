==================================
setuptools-build-subpackage v1.0.0
==================================

Package a subfolder as a python distribution

* Free software: Apache Software License 2.0

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Installation
============

::

    pip install setuptools-build-subpackage

You can also install the in-development version with::

    pip install https://github.com/ashb/setuptools-build-subpackage/archive/master.zip


Usage
=============

This distribution contains a subclass of setuptools's Distribution, designed to build a "sub-module" as a stand alone distribution.

It is designed to be used with `setuptools's declrative config <https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html>`_ -- i.e. where everything is defined in setup.cfg, not in setup.py

For example, take the following layout::

    ├── example
    │   ├── __init__.py
    │   ├── sub_module_a
    │   │   ├── __init__.py
    │   │   ├── setup.cfg
    │   │   └── where.py
    │   └── sub_module_b
    │       ├── __init__.py
    │       ├── setup.cfg
    │       └── where.py
    └── setup.cfg

This assumes we want ``example.sub_module_a`` and ``example.sub_module_b`` not included in the main distribution, but instead released as separate dists to PyPI.

This set of classes ensures the following:

- That the top level ``setup.cfg`` is not loaded, instead only the one specified from the sub-package
- That the ``build/`` folder for each sub-package is kept clean, so files from one build don't leak in to another
- That the ``setup.cfg`` from the sub-folder is present in the built ``sdist`` at the top level, meaning it can be installed normally.
- That a ``stub`` setup.py file is included for compatibility with older installers

Configure your main dist
------------------------

First you should exclude the sub-packages from being included in your main dist:

.. code-block:: python

    setup(
        ...
        packages=find_packages(exclude=['example.sub_module_*'])
    )

or

.. code-block:: ini

    [options.packages.find]
    exclude =
      example.sub_module_*

Create a setup.cfg for your sub-dist
------------------------------------

The requirements and information for the subdist are all driven off a setup.cfg -- right now a sub-``setup.py`` is not supported. (The ``setup.py`` included in the sdist will always be generated. PRs welcome if you need something else here.)

See ``example/sub_module_a/setup.cfg`` in the source code for a minimal example.

All file paths and module names are absolute, not relative to the location of the ``setup.cfg`` file

Build the sdist/bdist
---------------------

Run the following command:

.. code-block:: bash

    python -m setuptools_build_subpackage \
      --subpackage-folder example/sub_module_b \
      sdist \
      bdist_wheel

This will create a .tar.ga and .whl file in dist

Including a license comment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you need a license comment in the generated ``setup.py``, pass the ``--license-template`` option to ``sdist``


.. code-block:: bash

    python -m setuptools_build_subpackage \
      --subpackage-folder example/sub_module_b \
      sdist --license-template ./LICENSE \
      bdist_wheel

This argument should be a path to a plain-text license file, that will be included at the top of the generated file, each line prefixed with a python comment.

Development
===========

To run all the tests run::

    pip install -e '.[devel]' && pytest

It is also recommended that you install pre-commit to check style rules
