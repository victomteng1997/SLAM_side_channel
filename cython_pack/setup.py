from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [Extension("generateImagesCython",["generateImages_Cython.pyx"])]
setup(
    name = "generateImagesCython pyx",
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)