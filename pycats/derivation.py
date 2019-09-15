from pycats.database import query
derivations = []


class Derivation:
    def __init__(self, entity, context, accessor):
        self.entity = entity
        self.context = None if not context else sorted(context)
        self.accessor = accessor

        derivations.append(self)

    @classmethod
    def find_items(cls, entity, context):
        for x in derivations:
            if x.perfect_match(entity, context):
                return x.accessor(context)

        for x in derivations:
            if x.partial_match(entity, context):
                return x.accessor(context)

        for x in derivations:
            if x.identity_match(entity):
                return x.accessor(context)

        raise AttributeError(f"Cannot find identity derivation for '{entity}' in directory")


    def perfect_match(self, entity, context):
        return self.context and self.entity == entity and sorted([x for x in context]) == self.context

    def partial_match(self, entity, context):
        return self.context and self.entity == entity and all([x in context.keys() for x in self.context])

    def identity_match(self, entity):
        return self.entity == entity and self.context is None

    def __repr__(self):
        return "".join([self.entity, '->', ('*' if not self.context else '+'.join([x for x in self.context]))])
