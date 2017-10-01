#!/usr/bin/env python3

print('Welcome to our UDP chat.')
try:
    username = input('To get started, please provide a username: ')
    print(username)
except ValueError:
#    if not username:
    raise ValueError("Username can't be NULL")
