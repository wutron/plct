#!/usr/bin/env python
# package plct

files = ["bin",
         "python",
         "examples",

         "setup.py",
         "README.txt",
         "INSTALL.txt",
         "LICENSE.txt",
         "CHANGES.txt"]

exclude = [".*\.pyc$",
           "examples/ex_infeasible_transitive.tree",
           "examples/.*.plct"]

include = []

#=============================================================================

import os, sys, re, shutil
from subprocess import call, Popen, PIPE

pkgdir = sys.argv[1]

if os.path.exists(pkgdir):
    shutil.rmtree(pkgdir)

exclude_expr = "|".join(exclude)

p = Popen(["find", "-L"] + files, stdout=PIPE)
all_files = [x.rstrip("\n") for x in p.stdout.readlines()]
all_files = [x for x in all_files
             if not re.match(exclude_expr, x)] + include

for f in all_files:
    dest = os.path.join(pkgdir, f)
    destdir = os.path.dirname(dest)
    print f, "-->", dest

    if os.path.isfile(f):
        # copy file
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        shutil.copy(f, dest)
    else:
        # make dir
        if not os.path.exists(dest):
            os.makedirs(dest)

# tar
basename = os.path.basename(pkgdir)
print ' '.join(["tar", "-C", os.path.dirname(pkgdir), "-zcvf",
                pkgdir + ".tar.gz", basename])
call(["tar", "-C", os.path.dirname(pkgdir), "-zcvf",
      pkgdir + ".tar.gz", basename])

