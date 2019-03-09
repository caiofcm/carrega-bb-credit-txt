import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="parse_bb_credit",
    version="0.0.4",
    author="Caio Marcellos",
    author_email="caiocuritiba@gmail.com",
    description=("Parse BB .TXT file"),
    license="BSD",
    keywords="finance bb parse",
    #url="http://packages.python.org/an_example_pypi_project",
    packages=['parse_bb_credit'],  # , 'tests'
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
