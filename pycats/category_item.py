"""
A rough framework for dealing with interconnected fuzzy categories
of things, leveraging set theory and category theory.
"""

from pycats.derivation import Derivation

# When we make a new category, store it in here. On the individual categories,
# use helper function that returns metadata to implement a traversal point.
category_directory = {}

# When we make a new set, store it in here, indexed by name of the category
# it is a set of. On the individual categories, use helper function that
# returns metadata to implement a traversal point.
set_directory = {}


class CategoryItem:
    """
    An item within a particular category. The category is embedded in a network of categories,
    to and from which traversal occurs.
    """

    def __init__(self, identity, **context):
        """
        Record details about how we traversed to this point, as well as
        our current item's identity.
        """

        self._identity = self.__class__.__name__.lower()
        self.context = {k: v for k,v in context.items()}
        self.identity = str(identity)

    @classmethod
    def _category_set(cls, name):
        return set_directory[name]

    @classmethod
    def derivation(cls, context, accessor):
        Derivation(cls.__name__, context, accessor)

    @classmethod
    def set(cls):
        if not hasattr(cls, '_set'):
            cls._set = type(f"{cls.__name__}Set", (CategorySet,), {'single': cls})
        return cls._set

    # def __getattr__(self, item):
    #     """
    #     Intercept traversals out to other items and sets. These are dynamically
    #     defined, and can be circular.
    #     """
    #
    #     # Prevent recursive lookups, _item_jump_x, _item_jump_item_jump_x, etc etc
    #     if '_item_jump_' not in item and '_set_jump_' not in item:
    #
    #         # This is a traversal point to a single item.
    #         if hasattr(self, '_item_jump_'+item):
    #             traversal = getattr(self, '_item_jump_'+item)()
    #             return category_directory[traversal.target](
    #                 traversal.target_identity,
    #                 **{**self.context,
    #                    (self._identity if not traversal.assume_identity else traversal.assume_identity): self.identity}
    #             )
    #
    #         # This is a traversal point to a set of items.
    #         elif hasattr(self, '_set_jump_'+item):
    #
    #             traversal = getattr(self, '_set_jump_' + item)()
    #             ident_key = self._identity if not traversal.assume_identity else traversal.assume_identity
    #             pass_context = {**self.context, ident_key: self.identity}
    #             items = Derivation.find_items(set_directory[traversal.target].single.__name__, pass_context)
    #
    #             return set_directory[traversal.target](
    #                 items=(items if not traversal.target_identity else traversal.target_identity),
    #                 **pass_context
    #             )
    #
    #     # No attribute exists for this item and it is not a defined traversal point
    #     raise AttributeError

    @classmethod
    def open(cls, identity, **context):
        """
        Return a new instance of the class with identity and context as provided
        """

        return cls(identity, **context)

    def initial_load(self):
        """
        Loading that happens when an item is first opened
        """

        pass

    def late_load(self):
        """
        Loading that happens when an attribute of this item is accessed.
        """

        pass

    def __repr__(self):
        vals = [v for (k, v) in self.context.items()]
        return f"{self.__class__.__name__}({', '.join([self.identity, *vals])})"

    def __init_subclass__(cls, **kwargs):
        """
        Record subclasses of this CategoryItem in the category directory.
        """

        category_directory[cls.__name__] = cls


class CategorySet:
    """
    Represent a collection of CategoryItems.
    """

    def __init__(self, items=None, **context):
        """
        Record information about the items that are currently in this set.
        If items are passed into the items array, act as a container for those items
        """

        self.iterpos = 0
        self.context = context
        self.items = Derivation.find_items(self.single.__name__, context) if not items else items

    def __iter__(self):
        """
        Implement iterator protocol for this set
        """
        return self

    def __next__(self):
        """
        Implement iterator protocol for this set
        """

        if len(self.items) > self.iterpos:
            ret_item = self.items[self.iterpos]
            self.iterpos += 1
            return self.single.open(ret_item, **self.context)
        else:
            raise StopIteration

    def __call__(self, item):
        """
        Access a specific item in this set by the identity name of this item.
        """

        if item in self.items:
            return self.single.open(item, **self.context)
        else:
            raise ValueError

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(len(self.items)) + " " + self.single.__name__ + "s)"

    def __init_subclass__(cls, **kwargs):
        """
        Record subclasses of CategorySet in the set directory for use in dynamic traversal.
        """

        set_directory[cls.single.__name__] = cls
        set_directory[cls.__name__] = cls

    def __getitem__(self, item):
        return self.single.open(self.items[item], **self.context)