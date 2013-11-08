""" To be required by all test modules.
"""

import sys
import os

# Assume code lives in ../src/**
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.realpath(os.path.join(TEST_DIR, "..", "src"))

print "Configured import of src from"
print "\t%s" % SRC_DIR
