#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys


def signal_handler(signal, frame):
    sys.exit(0)


def cycle_sequence(seq):
    while True:
        yield from seq


signal.signal(signal.SIGINT, signal_handler)
for i in cycle_sequence(range(5)):
    print(i)
