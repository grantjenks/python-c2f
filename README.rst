Cython for All with GitHub Actions
==================================

TODO
----

- Add README sections for release workflow

- Use Sphinx: build docs for zoom-ability

- Add note about configuring secrets


Is Python interpreted or compiled?
----------------------------------


c2f.py
------

.. code-block:: python

   # cython: language_level=3
   "Celsius to Fahrenheit Library"

   def convert(celsius: float) -> float:
       "Convert Celsius to Fahrenheit"
       fahrenheit = celsius * 1.8 + 32
       return fahrenheit


setup.py
--------

.. code-block:: python

   from setuptools import setup
   from Cython.Build import cythonize

   setup(
       name='c2f',
       version='0.0.0',
       py_modules=['c2f'],
       ext_modules=cythonize('c2f.py'),
   )


c2f.cpython-38.pyc
------------------

.. code-block:: pycon

   >>> dis.dis(c2f.convert)
     6           0 LOAD_FAST                0 (celsius)
                 2 LOAD_CONST               1 (1.8)
                 4 BINARY_MULTIPLY
                 6 LOAD_CONST               2 (32)
                 8 BINARY_ADD
                10 STORE_FAST               1 (fahrenheit)
     7          12 LOAD_FAST                1 (fahrenheit)
                14 RETURN_VALUE


c2f.c
-----

.. code-block:: shell

   $ cython c2f.py

.. code-block:: c

   static PyObject * __pyx_pf_3c2f_convert(double __pyx_v_celsius) {
     double __pyx_v_fahrenheit;
     PyObject *__pyx_r = NULL;
     __pyx_v_fahrenheit = ((__pyx_v_celsius * 1.8) + 32.0);
     __pyx_r = PyFloat_FromDouble(__pyx_v_fahrenheit);
     return __pyx_r;
   }


c2f.so
------

.. code-block:: shell

   $ pip install wheel
   $ python setup.py bdist_wheel

.. code-block:: nasm

   ___pyx_pw_3c2f_1convert:
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


GitHub Workflow
---------------


Summmary
--------

Is Python an interpreted or compiled language? Trick question. It’s actually
both. With tools like Cython, we can take the compilation step further and
remove the interpreter loop almost entirely. Cython produces binaries much like
C++, Go, and Rust do. Now with GitHub Actions the cross-platform build and
release process can be automated for free for Open Source projects. This is an
enormous opportunity to make the Python ecosystem 20-50% faster with a single
pull request. The lightning talk will walk through a GitHub workflow that
publishes Cython-optimized wheels to PyPI. Discover how Cython can turbo-charge
your Python code and GitHub Actions can simplify your cross-platform release
process for free.


Appendix
--------

.. code-block:: shell

   $ gcc -g -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/Library/Frameworks/Python.framework/Versions/3.8/include/python3.8 -L/Library/Frameworks/Python.framework/Versions/3.8/lib -o c2f.so c2f.c -lpython3.8
   $ objdump -S -df=___pyx_pw_3c2f_1convert c2f.so
