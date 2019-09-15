"""
Classes for representing metadata about traversals between a set/item and another set/item
"""

class Traversal:
    """
    Record information about a traversal between a
    """
    def __init__(self, target, target_identity=None, assume_identity=None):
        self.target = target
        self.assume_identity = assume_identity
        self.target_identity = target_identity

class ItemTraversal(Traversal):
    def __init__(self, target, target_identity, assume_identity=None):
        super().__init__(target, target_identity, assume_identity)
        self.target_identity = target_identity

