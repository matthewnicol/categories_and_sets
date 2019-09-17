class ClassPropertyDescriptor:
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, instance, owner):
        if not owner:
            owner = type(instance)
        return self.fget.__get__(instance, owner)

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError('No setter defined')
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)
