Installation
=============

Basic Installation
--------------------------------
We have tested B-OCL with python 3.9+. We recommend creating a virtual environment (e.g. `venv <https://docs.python.org/3/tutorial/venv.html>`_,
`conda <https://docs.conda.io/en/latest/>`_).

Dependencies
************
B-OCL depends on BESSER for parsing the OCL constraints and providing a concrete syntax tree (CST) to evaluation. The latest stable version of BESSER is available in the Python Package Index (PyPi) and can be installed using

.. code-block:: console

    $ pip install besser


B-OCL Installation
******************

Stable version of B-OCL interpreter can be installed via

.. code-block:: console

    $ pip install bocl

.. note::
   B-OCL-Interpreter is compatible with VScode. It can be easily installed using VSCode terminal

Building From Source
--------------------
To obtain the full code, including examples and tests, you can clone the git repository.

.. code-block:: console

    $ git clone https://github.com/BESSER-PEARL/B-OCL-Interpreter
    $ cd B-OCL-Interpreter

To install the reqs please run the following commands in virtual environment (recommended)

.. code-block:: console

    $ pip install -r requirements.txt
