#!/usr/bin/env python
import sys

# Get input lines from stdin
for line in sys.stdin:
    # Remove spaces from beginning and end of the line
    line = line.strip()

    # Split it into words
    words = line.split()

    # Output tuples on stdout
    for word in words :
        print(word, "1")