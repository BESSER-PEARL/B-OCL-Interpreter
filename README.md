# BESSER Object Constraint Language Interpreter

**BOCL** is a tool designed to parse and evaluate the OCL constraints designed on **BESSER** models.
It is a python based implementation, that utilises parser and listener generated with the ANTLR4 grammer.

**BESSER** is a low-modeling low-code open-source platform built on top 
of our Python-based personal interpretation of a "Universal Modeling Language"

## Basic Installation
We have tested BOCL with python 3.9+. We recommend creating a virtual environment (e.g. `venv <https://docs.python.org/3/tutorial/venv.html>`_,
`conda <https://docs.conda.io/en/latest/>`_).

Dependencies
************
BOCL depends on BESSER for parsing the OCL constraints and providing a concrete syntax tree (CST) to evaluation. The latest stable version of BESSER is available in the Python Package Index (PyPi) and can be installed using


    $ pip install besser


# BOCL Installation


Stable version of BOCL interpreter can be installed via

    $ pip install bocl



## Building From Source

To obtain the full code, including examples and tests, you can clone the git repository.

    $ git clone https://github.com/BESSER-PEARL/BOCL-Interpreter
    $ cd BOCL-Interpreter

To install the reqs please run the following commands in virtual environment (recommended)

    $ pip install -r requirements.txt

## Contributing

We encourage contributions from the community and any comment is welcome!

If you are interested in contributing to this project, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Code of Conduct

At BESSER, our commitment is centered on establishing and maintaining development environments that are welcoming, inclusive, safe and free from all forms of harassment. All participants are expected to voluntarily respect and support our [Code of Conduct](CODE_OF_CONDUCT.md).

## Governance

The development of this project follows the governance rules described in the [GOVERNANCE.md](GOVERNANCE.md) document.

## Contact
You can reach us at: [info@besser-pearl.org](mailto:info@besser-pearl-org)

Website: https://besser-pearl.github.io/teampage/

## License

This project is licensed under the [MIT](https://mit-license.org/) license.
