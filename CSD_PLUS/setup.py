from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("model.py"))
setup(ext_modules=cythonize("node.py"))
setup(ext_modules=cythonize("runner.py"))