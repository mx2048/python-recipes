"""
Access the class scope from functions, comprehensions, or generator expressions
enclosed in that scope.

In Python 3, you cannot access the class scope from functions,
comprehensions, or generator expressions enclosed in that scope
except the outermost iterable.
"""

from collections import namedtuple


class Company:
    """Example"""

    # For Solution 1: Move KEYS to the global scope.
    __keys = ('name', 'shortcut', 'employees')
    KEYS = namedtuple('Keys', __keys)(*__keys)

    LLC = {KEYS.name: 'Limited liability company',
           KEYS.shortcut: 'LLC',
           KEYS.employees: 5,
           }
    INC = {KEYS.name: 'Corporation',
           KEYS.shortcut: 'INC',
           KEYS.employees: 5000,
           }

    __form_letters = [LLC, INC]

    # When running the script you get:
    # NameError: name 'KEYS' is not defined
    try:
        VALID_SHORTCUTS = {e[KEYS.shortcut]: e for e in __form_letters}
    except NameError:
        print('NameError caught.')

    # For solution 2: use lambda
    # VALID_SHORTCUTS = (lambda KEYS=KEYS, __form_letters=__form_letters:
    #                    {e[KEYS.shortcut]: e for e in __form_letters})()


# Solution 1:
# Move `KEYS` to global scope. This way no errors raise because
# `__form_letters` is the outermost iterable of the class.

# Solution 2:
# Define lambda.
