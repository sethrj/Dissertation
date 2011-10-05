#! /usr/bin/env python

# reactor_physicsify.py
# Seth R. Johnson
#
# Change TRT terminology to neutron transport terminology

import os
import re
import sys

substitutions = [
        (re.compile(r"(radiation\s+)?flux"), "current"),
        (re.compile(r"scalar\s+intensity"), "scalar flux"),
        (re.compile(r"(angular\s+)?intensity"), "angular flux"),
        (re.compile(r"opacit(y|ies)"), "cross section"),
        (re.compile(r"\bI\b"), r"\psi"),
        (re.compile(r"\bF\b"), r"J"),
#        (re.compile(r"\bc\b"), r"v"),
#        (re.compile(r"\bct\b"), r"vt"),
        ]

def replace_line(line):
    for (regex, replacement) in substitutions:
        line = regex.sub(replacement, line)
    return line

def global_replace(old_path):
    (base, ext) = os.path.splitext(old_path)
    new_path = "%s-rp%s" % (base, ext)

    with open( old_path, 'r') as old:
        with open( new_path, 'w') as new:
            for line in old:
                line = replace_line( line )
                new.write(line)

#******************************************************************************#
if __name__ == '__main__':
    if len(sys.argv) == 2:
        global_replace(sys.argv[1])
        sys.exit(0)

    print "Syntax: reactor_physicsify.py source_file"
    while True:
        inp = raw_input("Enter test input: ")
        inp = inp.strip()
        if inp:
            print "Result:", replace_line(inp)
        else:
            break

