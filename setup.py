from setuptools import setup
from Cython.Build import cythonize

setup(
    name='c2f',
    version='1.0.1',
    py_modules=['c2f'],
    ext_modules=cythonize('c2f.py'),
    long_description=open('README.rst').read(),
    long_description_content_type='text/plain',
)
