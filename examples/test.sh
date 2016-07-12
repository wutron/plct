#!/usr/bin/bash
#
# This is an example of how to use the PLCT program.
#
#
# Don't execute this script all at once.  Instead try copying and pasting each
# command to the command line one at a time to learn how the commands work.
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

# Call 'plct-feasible' with the files that you want to consider.
# Each file should contain a single tree in newick format.
# You may need to indicate the leaf label format through '-m'.
# ex_feasible.tree and ex_infeasible.tree contain the trees from the paper.
plct-feasible -m sli_ ex_feasible.tree ex_infeasible.tree

# The output is a tab-delimited file with the following columns:
#  0: filename
#     if the program is run with the '-d' flag, then files are identified
#     by their directory, e.g. a a file with name '<path>/<dir>/<basename>'
#     will be identified as '<dir>'
#  1: number of leaves in tree
#  2: number of species in tree
#  3: number of (species-specific) loci in tree
#  4: binary tree? (True/False)
#  5: trivially reconcilable? (True/False)
#     a tree is trivially reconcilable if no species contains more than one loci
#  6: reconcilable? (True/False)
#     whether the LEG is reconcilable
#     for binary trees,
#       LEG (ir)reconciliability implies tree (ir)reconciliability
#     for non-binary trees,
#       LEG irreconcilability implies tree irreconciliability
#       but LEG reconcilability implies unknown tree reconcibility
#  7: list of conflicting loci
#     each tuple corresponds to one irreconcilable connected component of the LEG
#     '-' indicates no conflicts

# Example Output
:<<EOF
ex_feasible.tree	6	2	3	True	False	True	-
ex_infeasible.tree	6	2	3	True	False	False	(b-1,b-2)
EOF

# You can also enter files through the '-i' option. Each argument to '-i'
# indicates a list of input files for plct-feasible to process.
plct-feasible -m sli_ -i infile.txt

# If '--outputext' is provided, the program will also output the PLCT and LEG.
# If the input file is named <basename><inputext>,
# then the output will be written to <basename><outputext>.
# For example, the following example will write to ex_infeasible.plct.
#
# This file has three sections:
#   PLCT
#     A tree in NHX format.
#     For branch (pnode, node), data is provided in the data for node.
#     Branches have the following data:
#       labels: comma-separated list, e.g. '(label1, label2, ...)'
#         species-specific locus labels for this branch
#       reconcilable: True/False
#         whether all labels on this branch are pairwise reconcilable
#         defined only for non-leaf branches with labels
#       reconcilable_cc: True/False
#         whether all labels on this branch are part of reconcialble CC of LEG
#         defined only for branches with labels
#   LEG
#     An adjacency list. Each line consists of tab-delimited list of nodes.
#     The first label is the source node. Further labels are target nodes
#     and indicate an edge between source and target.
#   CC
#     A list of connected components of the LEG. Each line consists of a
#     tab-delimited list of nodes in one connected component of the LEG,
#     followed by a True/False boolean indicating whether the component
#     is reconcilable.
plct-feasible -m sli_ --inputext .tree --outputext .plct ex_infeasible.tree

