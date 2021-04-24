# -*- encoding: utf-8 -*-

__author__ = 'brian'

import random
import string


def contrasena_generator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))