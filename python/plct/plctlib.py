import collections
import networkx as nx

from rasmus import treelib

class Label:
    """Species-specific locus"""

    def __init__(self, species, locus):
        self.species = species
        self.locus = locus

    def __str__(self):
        return self.species + '-' + self.locus

    def __repr__(self):
        return "<label %s-%s>" % (self.species, self.locus)    

    def __eq__(self, other):
        return (self.species == other.species) and (self.locus == other.locus)

    def __cmp__(self, other):
        return cmp((self.species, self.locus), (other.species, other.locus))

    def __hash__(self):
        return hash((self.species, self.locus))
        

def is_reconcilable(tree, mapping='sli',
                    annotate=False, return_conflicts=False, return_leg=False):
    """Given a tree, returns True if there exists conficting loci and False otherwise."""
    groupings = group_leaves(tree, mapping)
    create_plct(tree, groupings)
    leg = create_leg(tree, groupings)
    conflicts = get_conflicts(leg)
    flag_reconcilable = (len(conflicts) == 0)

    if annotate:
        annotate_tree(tree, conflicts)

    return_vals = (flag_reconcilable,)
    if return_conflicts:
        return_vals = return_vals + (conflicts,)
    if return_leg:
        return_vals = return_vals + (leg,)
    return return_vals


def group_leaves(tree, mapping='sli'):
    """Returns dictionary with genes from same species and locus grouped together.

    key = (species,locus)
    value = list of gene tree nodes at this species and locus
    """
    # collect leaves based on species and locus
    groupings = collections.defaultdict(list)
    for leaf in tree.leaves():
        if mapping == 'sli':
            species, locus, ind = leaf.name.split('-') # leaf format = "species-locus-ind"
        elif mapping == 'sil':
            species, ind, locus = leaf.name.split('-') # leaf format = "species-ind-locus"
        elif mapping == 'sli_':
            species, locus, ind = leaf.name.split('_') # leaf format = "species_locus_ind"
        elif mapping == 'sil_':
            species, ind, locus = leaf.name.split('_') # leaf format = "species_ind_locus"
        else:
            raise Exception("mapping not supported: %s" % mapping)

        label = Label(species, locus)
        groupings[label].append(leaf)

    return groupings


def create_plct(tree, groupings, new_copy=False):
    """Creates plct for tree using groupings."""
    if new_copy:
        tree = tree.copy()

    for node in tree:
        node.data["labels"] = set()

    for label, genes in groupings.iteritems():
        lca = treelib.lca(genes)
        for leaf in genes:
            # follows each leaf up and labels branch by storing color in node data
            travel = leaf
            while travel != lca:
                # add label to branch
                travel.data["labels"].add(label)
                travel = travel.parent
    return tree


def create_leg(plct, groupings):
    """Creates leg from plct and groupings."""
    leg = nx.Graph()
    leg.add_nodes_from(groupings.keys()) # nodes = Label(species, locus)
    for node in plct:
        labels = list(node.data["labels"]) # convert label set to label list
        nlabels = len(labels)
        for i in xrange(nlabels):
            for j in xrange(i+1, nlabels):
                assert labels[i] in leg and labels[j] in leg
                leg.add_edge(labels[i], labels[j])
    return leg


def get_conflicts(leg):
    """Find irreconcilable connected components of leg."""
    conflicts = set() # connected components with conflict
    for cc in nx.connected_components(leg):
        # key = species, val = set of loci in species for this cc
        loci_dct = collections.defaultdict(set)

        for label in cc:
            loci_dct[label.species].add(label.locus)

        for sp, loci in loci_dct.iteritems():
            # conflict if a species has more than one loci in this cc
            if len(loci) >= 2:
                conflicts.add(tuple(sorted(cc)))
                break
    return conflicts


def annotate_tree(tree, conflicts):
    """Annotate tree."""
    # reconcilable => no labels on this branch are pairwise irreconcilable
    # reconcilable_cc => no labels on this branch are part of irreconcilable cc of leg
    conflicting_labels = set()
    for cc in conflicts:
        conflicting_labels.update(cc)

    for node in tree:
        labels = node.data["labels"]
        if not labels:
            continue

        node.data["reconcilable_cc"] = True
        loci_dct = collections.defaultdict(set)
        for label in labels:
            if label in conflicting_labels:
                node.data["reconcilable_cc"] = False
            loci_dct[label.species].add(label.locus)

        if node.is_leaf(): # a leaf always has a single label
            continue       # so there are no pairs to consider
        node.data["reconcilable"] = True
        for sp, loci in loci_dct.iteritems():
            # conflict if a species has more than one loci
            if len(loci) >= 2:
                node.data["reconcilable"] = False
