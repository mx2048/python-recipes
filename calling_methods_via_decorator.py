from functools import wraps
from typing import Collection, Set


def apply_for(attribute: str, included: Collection[str]=None, excluded: Collection[str]=None):
    """
    Decorator: Call a decorated method of a class having `attribute`
    only when the attribute's value is in the `included` list
    and not in the `excluded` one.

    If the `included` collection is empty or None the `attribute` is not
    in the `excluded` collection, always call the decorated method.

    Usage:
    @apply_for(attribute='fruit', included='Apple, Carrot')
    def peel(self):
        pass
    """
    def args_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            def uniform(value: str) -> str:
                return value.strip().upper()

            def normalize_to_set(argument: Collection[str]) -> Set[str]:
                if isinstance(argument, str):
                    sep = ',' if ',' in argument else ' '
                    argument = argument.split(sep)
                argument = {uniform(e) for e in argument}
                return argument

            # Do not rewrite the nonlocal arguments.
            nonlocal attribute, included, excluded

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
    return args_wrapper


if __name__ == '__main__':

    class ProgrammingLanguage:
        def __init__(self, language):
            self.language = language
            self.data = 'No kudos yet'

        @apply_for(attribute='language', included=['Python', 'C'], excluded='Java')
        def add_kudos(self, value):
            self.data = f'Kudos acquired: {value} '

    for language in ['python', 'c', 'java', 'Perl']:
        obj = ProgrammingLanguage(language)
        obj.add_kudos('100')
        print(f'{obj.language.capitalize()} - {obj.data}')

    # Output:
    # Python - Kudos acquired: 100
    # C - Kudos acquired: 100
    # Java - No kudos yet
    # Perl - No kudos yet

    # Note, method `add_kudos` was called only for included languages.
    # The `ProgrammingLanguage` has attribyte `self.language` which name was
    # passed in `@apply_for()` decorator.
