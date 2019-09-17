derivations = []


class Derivation:
    """
    A definition of what items are in a set given the context it was accessed from.
    """

    def __init__(self, category, context, accessor):
        """
        Define a derivation for category given a context and optional lookup name.

        :param category: The object the lookup is performed on
        :param context: A list of category names expected in the context
        :param accessor: Function (context, (lookup_name (optional)) => a list of identities in set
        """

        self.category = category
        self.context = None if not context else sorted(context)
        self.accessor = accessor

        derivations.append(self)

    @classmethod
    def find_items(cls, entity, context, lookup_name=None):
        """
        Sort through all defined derivations for this entity, and return the optimal accessor given the context

        Perfect Match = All context items existing are defined in the derivation
        Partial Match = All context items existing are defined in the derivation, but also unrelated context
        Identity Match = It is just the entity, no context matches

        :param entity: The category we are looking up on
        :param context: The context in which we're doing the lookup.
        :param lookup_name: Optional unique name specified by traversal point a.

        :return: Items in CategorySet, as defined by the winning derivation's accessor
        """

        # Aim for perfect match, try for partial match, eventually resort to identity match
        for d in ['perfect_match', 'partial_match', 'identity_match']:
            for x in derivations:
                if getattr(x, d)(entity, context):
                    try:
                        return x.accessor(context, lookup_name)
                    except TypeError:
                        return x.accessor(context)

        raise AttributeError(f"Cannot find identity derivation for '{entity}' in directory")

    def perfect_match(self, entity, context):
        return self.context and self.category == entity and sorted([x for x in context]) == self.context

    def partial_match(self, entity, context):
        return self.context and self.category == entity and all([x in context.keys() for x in self.context])

    def identity_match(self, entity, context):
        return self.category == entity and self.context is None

    def __repr__(self):
        return "".join([self.category, '->', ('*' if not self.context else '+'.join([x for x in self.context]))])
