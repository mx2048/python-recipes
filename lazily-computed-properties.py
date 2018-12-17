"""
Define an attribute as a property that only gets computed on access once,
then the attribute is cached and returned from the cache on every access
including initializing additional instances of the parent class
and of the subclasses.
"""


class LazyProperty:
    """
    Class as a property decorator around methods computed only once on access.

    Consequent instantiating of the underlying class with the decorated methods
    or the subclasses inheriting from the underlying class return the computed
    values from the underlying class `__dict__`.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(cls)
            setattr(cls, self.func.__name__, value)
            return value


if __name__ == '__main__':
    pass
