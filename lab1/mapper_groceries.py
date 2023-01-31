#!/usr/bin/env python
import sys

onlydata = sys.stdin
next(onlydata) # skip first line of input file

# Get input lines from stdin
for line in onlydata:
    # Remove spaces from beginning and end of the line
    line = line.strip()
    data = line.split(",")

    # Split it into words
    word = data[2]

    # Output tuples on stdout
    print(word, "1")