#!/usr/bin/bash
#
# This is an example of how to use the PLCT program.
#
#
# Don't execute this script all at once.  Instead try copying and pasting
# each command to the command line one at a time in order to learn how the
# commands work.
#

#=============================================================================
# setup/install

# Make sure tools are compiled and installed before running the commands in
# this tutorial.  See INSTALL.txt for more information.

# Or you can run from the source directory:

cd ..
python setup.py install

cd examples
export PATH=$PATH:../bin
export PYTHONPATH=$PYTHONPATH:../python


#=============================================================================
# determine reconciliation feasibility

# Call 'plct-conflict' with the files that you want to consider.
# Each file should contain a single tree in newick format.
# You may need to indicate the leaf label format through '-m'.
# ex_feasible.tree and ex_infeasible.tree contain the newick trees from the paper.
plct-conflict -m sli_ ex_feasible.tree ex_infeasible.tree

# The output is a tab-delimited file with the following columns:
#  0: filename
#  1: number of leaves in tree
#  2: number of species in tree
#  3: number of (species-specific) loci in tree
#  4: trivially reconcilable? (True/False)
#     a tree is trivially reconcilable if no species contains more than one loci
#  5: reconcilable? (True/False)
#  6: list of conflicting loci
#     each tuple corresponds to one irreconcilable connected component of the LEG
#     '-' indicates no conflicts

# Example Output
:<<EOF
ex_feasible.tree        6       2       3       False   True	-
ex_infeasible.tree	6	2	3	False	False	(b-1,b-2)
EOF

# You can also enter files through the '-i' option.
# Each argument to '-i' indicates a list of input files for plct-conflict to process.
plct-conflict -m sli_ -i infile.txt

# If '--outputext' is provided, plct will additionally process the gene tree
# and annotate each branch with the following:
#   labels:          species-specific locus labels for this branch
#   reconcilable:    whether all labels on this branch are pairwise reconcilable (True/False)
#                    defined only for non-leaf branches with labels
#   reconcilable_cc: whether all labels on this branch are part of reconcialble CC of LEG (True/False)
#                    defined only for branches with labels
# For branch (pnode, node), the annotation for the branch is provided in the data for node.
# The annotation is written in NHX format.
plct-conflict -m sli_ --outputext .plct ex_infeasible.tree

