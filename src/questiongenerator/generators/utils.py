
import random


def get_random_number (include, exclude=[]):
    """Generates a random number.

        Args:
            include: If it's a list, the posible choices, if it's a number the choices will be between -include and +include.
            exclude: Choices to exclude from the include list.
        Returns:
            A random number among the specified by include paramenter.
    """
    include_list = list(include) if type(include) is list else range_list(include)
    for num in exclude:
        try:
            include_list.remove(num)
        except ValueError:
            continue
    return random.choice(include_list)

def range_list(a, b=None):
    """ Return the range list between a and b """
    if b is None:
        return list(range(-a,a))
    return list(range(a,b))
