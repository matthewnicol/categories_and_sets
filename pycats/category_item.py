"""
A rough framework for dealing with interconnected fuzzy categories
of things, leveraging set theory and category theory.
"""
from pycats.clsmethod_descriptor import classproperty
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
        self.context = {k: v for k, v in context.items()}
        self.identity = str(identity)

    @classmethod
    def category_set(cls, name):
        return set_directory[name]

    @classmethod
    def category_item(cls, name):
        return category_directory[name]

    @classmethod
    def derivation(cls, context, accessor):
        Derivation(cls.__name__, context, accessor)

    @classproperty
    def set(cls):
        return type(f"{cls.__name__}Set", (CategorySet,), {'single': cls})

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
        context = [v for (k, v) in self.context.items()]
        return f"{self.__class__.__name__}({', '.join([self.identity, *context])})"

    def __init_subclass__(cls, **kwargs):
        """
        Record subclasses of this CategoryItem in the category directory.
        Also make the set so that the user doesn't have to explicitly define it
        """

        category_directory[cls.__name__] = cls
        set_directory[cls.__name__] = cls.set()


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

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            if sorted(other.items) == sorted(self.items):
                return True

    @classmethod
    def category_set(cls, name):
        return set_directory[name]

    @classmethod
    def category_item(cls, name):
        return category_directory[name]
