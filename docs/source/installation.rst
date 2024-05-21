Installation
=============

Basic Installation
--------------------------------
We have tested BOCL with python 3.9+. We recommend creating a virtual environment (e.g. `venv <https://docs.python.org/3/tutorial/venv.html>`_,
`conda <https://docs.conda.io/en/latest/>`_).

Dependencies
************
BOCL depends on BESSER for parsing the OCL constraints and providing a concrete syntax tree (CST) to evaluation. The latest stable version of BESSER is available in the Python Package Index (PyPi) and can be installed using

.. code-block:: console

    $ pip install besser


BOCL Installation
******************

Stable version of BOCL interpreter can be installed via

.. code-block:: console

    $ pip install bocl



Building From Source
--------------------
To obtain the full code, including examples and tests, you can clone the git repository.

.. code-block:: console

    $ git clone https://github.com/BESSER-PEARL/BOCL-Interpreter
    $ cd BOCL-Interpreter

To install the reqs please run the following commands in virtual environment (recommended)

.. code-block:: console

    $ pip install -r reqs.txt
