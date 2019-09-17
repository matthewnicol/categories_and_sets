""" Represents the links between the various sets and items, defined mainly on CategoryItems
"""

class Traversal:
    """ Metadata about the traversal from a CategoryItem to a set for a different category
    """
    def __init__(self, target, rename_this=None, fixed_items=None, lookup_key=None):
        """
        :param target: The name of the set this link traverses to
        :param rename_this: Use different category name in context post-traversal
        :param fixed_items: Override derivation, specifying the full space of the set
        """
        self.target = target
        self.rename_from = rename_this
        self.fixed_items = fixed_items
        self.lookup_key = lookup_key

    def __get__(self, instance, owner):
        """
        Lookup the target and instantiate as a set.
        :returns: CategorySet
        """
        x = owner.category_set(self.target)
        return x(
            items=self.fixed_items,
            **instance.context,
            **{self.rename_from if self.rename_from else owner.__name__.lower(): instance.identity},
            LOOKUP_NAME=self.lookup_key
        )


class ItemTraversal(Traversal):
    """ Metadata about the traversal from a CategoryItem to a different CategoryItem
    """
    def __init__(self, target, identity, assume_identity=None):
        super().__init__(target, identity, assume_identity)
        self.target_identity = identity

    def __get__(self, instance, owner):
        """
        Lookup the target and instantiate as a category
        :returns: CategoryItem
        """
        identity = self.target_identity if not callable(self.target_identity) else self.target_identity(instance.context)
        x = owner.category_item(self.target)

        return x(
            identity,
            **instance.context,
            **{self.rename_from if self.rename_from else owner.__name__.lower(): instance.identity}
        )


