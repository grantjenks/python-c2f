from setuptools import setup
from Cython.Build import cythonize

setup(
    name='c2f',
    version='1.0.3',
    py_modules=['c2f'],
    ext_modules=cythonize('c2f.py'),
    long_description=open('README.rst').read(),
)
