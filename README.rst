Cython for All with GitHub Actions
==================================

Is Python an interpreted or compiled language? Trick question. It’s actually
both. With tools like Cython, we can take the compilation step further and
remove the interpreter loop almost entirely. Cython produces binaries much like
C++, Go, and Rust do. Now with GitHub Actions the cross-platform build and
release process can be automated for free for Open Source projects. This is an
enormous opportunity to make the Python ecosystem 20-50% faster with a single
pull request. This lightning talk will walk through a GitHub workflow that
publishes Cython-optimized wheels to PyPI. Discover how Cython can turbo-charge
your Python code and GitHub Actions can simplify your cross-platform release
process for free.


SF Python Holiday Party 2019
----------------------------

| Grant Jenks
| Dec. 4, 2019
| `github.com/grantjenks/python-c2f`_


Is Python interpreted or compiled?
----------------------------------

| .
| .
| .
| ?
| .
| .
| .
| ?
| .
| .
| .
| ?


c2f.py
------

.. code-block:: python
   :linenos:
   :emphasize-lines: 5

   "Celsius to Fahrenheit Library"

   def convert(celsius: float) -> float:
       "Convert Celsius to Fahrenheit"
       fahrenheit = celsius * 1.8 + 32
       return fahrenheit


c2f.cpython-38.pyc
------------------

.. code-block:: pycon
   :linenos:
   :emphasize-lines: 2

   >>> import c2f
   >>> dis.dis(c2f.convert)
     6           0 LOAD_FAST                0 (celsius)
                 2 LOAD_CONST               1 (1.8)
                 4 BINARY_MULTIPLY
                 6 LOAD_CONST               2 (32)
                 8 BINARY_ADD
                10 STORE_FAST               1 (fahrenheit)
     7          12 LOAD_FAST                1 (fahrenheit)
                14 RETURN_VALUE


setup.py
--------

.. code-block:: python
   :linenos:
   :emphasize-lines: 2, 8

   from setuptools import setup
   from Cython.Build import cythonize

   setup(
       name='c2f',
       version='0.0.0',
       py_modules=['c2f'],
       ext_modules=cythonize('c2f.py'),
   )


c2f.c
-----

.. code-block:: shell

   $ cython c2f.py

.. code-block:: c
   :linenos:
   :emphasize-lines: 5

   static PyObject * __pyx_convert(double __pyx_v_celsius)
   {
     double __pyx_v_fahrenheit;
     PyObject *__pyx_r = NULL;
     __pyx_v_fahrenheit = ((__pyx_v_celsius * 1.8) + 32.0);
     __pyx_r = PyFloat_FromDouble(__pyx_v_fahrenheit);
     return __pyx_r;
   }


c2f.so
------

.. code-block:: shell

   $ python setup.py bdist_wheel

.. code-block:: nasm
   :linenos:
   :emphasize-lines: 6, 7

   ___pyx_convert:
   push	  rbp
   mov	  rbp, rsp
   sub	  rsp, 16
   movsd  xmm0, qword ptr [rbp - 8]
   mulsd  xmm0, qword ptr [rip + 1379]
   addsd  xmm0, qword ptr [rip + 1379]
   call	  502 <PyFloat_FromDouble ...>
   add	  rsp, 16
   pop	  rbp
   ret


.github/workflows/release.yml
-----------------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 5, 9

   name: release
   on:
     push:
       tags:
         - v*
   jobs:
     build-linux-cp38:
       runs-on: ubuntu-latest
       container: quay.io/pypa/manylinux2014_x86_64
       steps:
       ...


Matrix Build
------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 4, 5, 6

   build-macos:
     runs-on: macos-latest
     strategy:
       max-parallel: 4
       matrix:
         python-version: [3.5, 3.6, 3.7, 3.8]
     steps:
     ...


Mac Build Steps
---------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 1, 7, 10

   - name: Set up Python ${{ matrix.python-version }} x64
     uses: actions/setup-python@v1
     with:
       python-version: ${{ matrix.python-version }}
       architecture: x64

   - name: Install package dependencies
     run: pip install cython wheel

   - name: Build binary wheel
     run: python setup.py bdist_wheel


Store Build Artifacts
---------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 2

   - name: Archive dist artifacts
     uses: actions/upload-artifact@v1
     with:
       name: dist-macos-${{ matrix.python-version }}
       path: dist


Linux auditwheel Tool
---------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 1, 4, 7

   - name: Build binary wheel
     run: /opt/python/cp38-cp38/bin/python setup.py bdist_wheel

   - name: Apply auditwheel for manylinux wheel
     run: auditwheel repair -w dist dist/*

   - name: Remove linux wheel
     run: rm dist/*-linux_x86_64.whl


Windows Build Steps
-------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 1, 4

   - name: Download Build Tools for Visual Studio 2019
     run: Invoke-WebRequest -Uri https://aka.ms/vs/16/rel...

   - name: Run vs_buildtools.exe install
     run: ./vs_buildtools.exe --quiet --wait --norestart ...


Source Distribution
-------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 2, 6, 9

   upload:
     needs: [build-linux-cp35, ...]
     runs-on: ubuntu-latest
     steps:
     ...
     - name: Install dependencies
       run: pip install -r requirements.txt

     - name: Create source dist
       run: python setup.py sdist


Stage Binary Wheels
-------------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 2, 4, 5

   - name: Stage linux 3.8
     uses: actions/download-artifact@v1
     with:
       name: dist-linux-3.8
   - run: mv -v dist-linux-3.8/* dist/

   - name: Stage macos 3.8
     uses: actions/download-artifact@v1
     with:
       name: dist-macos-3.8
   - run: mv -v dist-macos-3.8/* dist/
   ...


Upload with Twine
-----------------

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 3, 4, 8

   - name: Upload with twine
     env:
       TWINE_USERNAME: ${{ secrets.TWINE_USERNAME }}
       TWINE_PASSWORD: ${{ secrets.TWINE_PASSWORD }}
     run: |
       ls -l dist/*
       pip install twine
       twine upload dist/*


Cythonize all the Things!
-------------------------

| Grant Jenks
| Dec. 4, 2019
| `github.com/grantjenks/python-c2f`_

*Cythonize all the Things!*

*Cythonize all the Things!*

*Cythonize all the Things!*

*Cythonize all the Things!*

*Cythonize all the Things!*

*Cythonize all the Things!*

.. _github.com/grantjenks/python-c2f: https://github.com/grantjenks/python-c2f/


Appendix
--------

Dumping Assembly
................

.. code-block:: shell

   $ gcc -g -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/Library/Frameworks/Python.framework/Versions/3.8/include/python3.8 -L/Library/Frameworks/Python.framework/Versions/3.8/lib -o c2f.so c2f.c -lpython3.8
   $ objdump -S -df=___pyx_pw_3c2f_1convert c2f.so


Git Tagging
...........

.. code-block:: shell

   $ git tag -a v0.0.2 -m v0.0.2
   $ git push --tags
