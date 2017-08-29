import random
import string

from .headerdict import HeaderDict  # NOQA
from .cached_property import cached_property  # NOQA


def random_string(len=32, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for x in range(len))
