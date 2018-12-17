"""
Define an attribute as a property that only gets computed on access once,
then the attribute is cached and returned from the cache on every access
including initializing additional instances of the parent class
and of the subclasses.

Note that in the example the attribute `a` is computed via the method.
As a matter of good practice, the result of the __init__ method must be a fully
initialized object. What that means is that the object must be ready for use;
it should not require some other settings to be tweaked or methods
to be executed before it can perform its function.

Credits:
D. M. Beazley and B. K. Jones, Python cookbook
W. Badenhorst, Practical Python Design Patterns
"""


class lazyproperty:
    """
    Class as a property decorator around methods computed only once on access.

    Consequent instantiatings of the underlying class with the decorated
    methods or the subclasses inheriting from the underlying class
    return the computed values from the underlying class `__dict__`.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(cls, self.func.__name__, value)
            return value


if __name__ == '__main__':

    class A:
        def __init__(self):
            self.a = self.slow_method
            pass

        @lazyproperty
        def slow_method(self):
            print('Slow method is performing...')
            return 1


    class B(A):
        def __init__(self):
            super().__init__()
            self.b = 2


    a = A()
    b = B()

    print(a.a)
    print(b.a)
    print(A().slow_method)
    print(b.slow_method)

    # Output:

    # Slow method is performing...
    # 1
    # 1
    # 1
    # 1

    # Notice the slow method is computed only once.
