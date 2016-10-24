from distutils.core import setup
# from Cython.Build import cythonize
from distutils.extension import Extension

from Cython.Distutils import build_ext

ext_modules = [Extension("filtration",
              ["filtration.pyx"],
              libraries=["m"],
              extra_compile_args=["-ffast-math"])]
setup(

    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
    # ext_modules = cythonize("filtration.pyx")
)
