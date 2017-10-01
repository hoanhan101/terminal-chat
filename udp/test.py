#!/usr/bin/env python3

while True:
    try:
        user_input = input("username: ")
        if not user_input:
            raise ValueError('empty string')
        else:
            break
    except ValueError as e:
        print(e)
