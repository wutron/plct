#!/usr/bin/env python
#
# setup for PLCT library packages
#
# use the following to install:
#   python setup.py install
#

import os,sys
from distutils.core import setup

sys.path.insert(0, os.path.realpath(
            os.path.join(os.path.dirname(__file__), "python")))
import plct
VERSION = plct.PROGRAM_VERSION_TEXT

setup(
    name='plct',
    version=VERSION,
    description='PLCT',

    author='Yi-Chieh Wu',
    author_email='yjw@cs.hmc.edu',
    url='http://www.cs.hmc.edu/~yjw/software/plct/',
    download_url='http://www.cs.hmc.edu/~yjw/software/plct/pub/sw/plct-%s.tar.gz' % VERSION,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        ],

    package_dir = {'': 'python'},
    packages=['plct',
              'plct.deps.rasmus'],
    py_modules=[],
    scripts=['bin/plct-feasible'],
    ext_modules=[]
    )
