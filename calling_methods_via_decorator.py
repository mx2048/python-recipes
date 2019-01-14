from functools import wraps
from typing import Collection, Set


def call_for(attribute: str, *, included: Collection[str]=None, excluded: Collection[str]=None):
    """
    Decorator: Call a decorated method of a class having `attribute`
    only when the attribute's value is in the `included` list
    and not in the `excluded` one.

    If the `included` collection is empty or None, and the `attribute` is not
    in the `excluded` collection, always call the decorated method.

    Usage:
    @call_for(attribute='fruit', included='Apple, Carrot')
    def peel(self):
        pass

    where `self.fruit` must be 'apple' or 'carrot'
    for method `peel` to be called.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            def uniform(value: str) -> str:
                return str(value).upper()

            def normalize_to_set(param: Collection[str]) -> Set[str]:
                if isinstance(param, str):
                    param = param.replace(',', ' ').split()
                param = {uniform(e) for e in param}
                return param

            self, *_ = args
            attr_value = getattr(self, attribute)
            attr_value = uniform(attr_value)

            if included:
                included_set = normalize_to_set(included)
                if attr_value not in included_set:
                    return None
            if excluded:
                excluded_set = normalize_to_set(excluded)
                if attr_value in excluded_set:
                    return None

            return func(*args, **kwargs)
        return wrapper
    return decorate


if __name__ == '__main__':

    class ProgrammingLanguage:
        def __init__(self, language):
            self.language = language
            self.data = 'No kudos yet'

        @call_for(attribute='language', included='Python, C', excluded='Java')
        def add_kudos(self, value):
            self.data = f'Kudos acquired: {value}'

        @call_for('language', included='Java')
        def deduct_kudos(self):
            self.data = 'Kudos deducted'

    for lang in ['python', 'c', 'java', 'Perl']:
        obj = ProgrammingLanguage(lang)
        obj.add_kudos('100')
        obj.deduct_kudos()
        print(f'{obj.language.capitalize()} - {obj.data}')

    # Output:
    # Python - Kudos acquired: 100
    # C - Kudos acquired: 100
    # Java - Kudos deducted
    # Perl - No kudos yet

    # Note, method `add_kudos` was called only for included languages.
    # The `ProgrammingLanguage` has attribute `language` which name was
    # passed in `@call_for()` decorator.

    # Caveats:
    #
    # Do not rewrite the parameters passed
    # to the outermost function `call_for` inside inner functions.
    # You will get UnboundLocalError.
