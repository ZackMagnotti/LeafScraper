from anytree import NodeMixin, RenderTree


class Strain:

    def __init__(self, name, url):

        self._name = name
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url
    

class StrainAncestorNode(Strain, NodeMixin):

    def __init__(self, name, url, strain_child=None, strain_parents=None):
        """
        ------------------------------------
        IMPORTANT NOTE
        ------------------------------------
        The anytree library (and most tree data structures)
        use the term "parent" to refer to a node above the
        current node in the tree, and children to refer to the
        nodes directly below.

        This is the reverse orientation of the StrainNode
        terminology, in which the lower levels of the tree are the
        "parents", and those above are the "children".

        You will see throughout this class some confusing
        looking variable assigments and function definitions.
        These are due to the "normal" and "strain" version of
        lineage being the reverse of eachother.

        example :     parent == strain_child
                    children = strain_parents
        ------------------------------------
        """
        Strain.__init__(self, name, url)
        self.parent = strain_child
        if strain_parents:
            self.children = strain_parents

    @property
    def strain_child(self):
        return self.parent

    @strain_child.setter
    def strain_child(self, strain_child):
        self.parent = strain_child

    @property
    def strain_parents(self):
        return self.children

    @strain_parents.setter
    def strain_parents(self, strain_parents):
        self.children = strain_parents

    @strain_parents.deleter
    def strain_parents(self, strain_parents):
        del self.children

    @property
    def strain_descendants(self):
        return self.ancestors

    @property
    def strain_ancestors(self):
        return self.descendants
    
    @property
    def co_parents(self):
        '''
        Tuple of strains who all parent the same child
        '''
        return self.siblings

    def show_tree(self):
        print(RenderTree(self).by_attr('name'), '\n')
    

class StrainDescendantNode(Strain, NodeMixin):

    def __init__(self, name, url, parent=None, children=None):
        '''
        NOT YET IMPLEMENTED

        Fills the opposite role as StrainAncestryNode

        Data Structure meant for organizing all the 
        descendents of a given strain
        '''
        Strain.__init__(self, name, url)
        self.parent = parent
        if children:
            self.children = children

    def show_tree(self):
        print(RenderTree(self).by_attr('name'), '\n')