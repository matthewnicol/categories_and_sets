"""
Classes for representing metadata about traversals between a set/item and another set/item
"""


class Traversal:
    """
    Record information about a traversal between a
    """
    def __init__(self, target, rename_this=None, fixed_items=None):
        self.target = target
        self.rename_from = rename_this
        self.fixed_items = fixed_items

    def __get__(self, instance, owner):
        x = owner.category_set(self.target)
        return x(
            items=self.fixed_items,
            **instance.context,
            **{self.rename_from if self.rename_from else owner.__name__.lower(): instance.identity}
        )


class ItemTraversal(Traversal):
    def __init__(self, target, target_identity, assume_identity=None):
        super().__init__(target, target_identity, assume_identity)
        self.target_identity = target_identity

