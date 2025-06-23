#!/usr/bin/env python3

import random
import string

def Password(length=32):
    chars = string.digits + string.ascii_letters  # 0-9 + a-z + A-Z
    return ''.join(random.choice(chars) for _ in range(length))

print(Password())
