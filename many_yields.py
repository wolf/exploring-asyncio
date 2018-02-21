#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def bottom():
    # Returning the yield lets the value that goes up the call stack, to come right back down
    return (yield 42)

def middle():
    return (yield from bottom())

def top():
    return (yield from middle())

# Get the generator.
gen = top()
value = next(gen)
print(value)  # prints '42'.
try:
    value = gen.send(value * 2)
except:
    ...
# except StopIteration as exc:
    # value = exc.value

print(value)  # Prints '84'.
