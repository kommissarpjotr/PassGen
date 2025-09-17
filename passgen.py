#!/usr/bin/env python3

import random
import string

# Simple and effective password without special characters 
def Password(length=32):
    chars = string.digits + string.ascii_letters  # 0-9 + a-z + A-Z
    return ''.join(random.choice(chars) for _ in range(length))

# Password with Special characters, usualy more secure
def PassPlus(length=32):
    chars = string.digits + string.ascii_letters + string.punctuation # 0-9 + a-z + A-Z + all punctuation
    return ''.join(random.choice(chars) for _ in range(length))

print("Password:", Password()) 
print("PassPlus:", PassPlus())
