#!/usr/bin/python

import subprocess

import github3

import os
import sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option('--name', '-n', type='string', help='Help or this option', action='store')
parser.add_option('--build_script', '-b', type='string', help='Help build script', action='store')
parser.add_option('--verbose', '-v', '--ver', type='string', help='verbose mode', default=False)

(options, args) = parser.parse_args()

print( sys.argv[0] )

sys.exit(0)



if len(args) != 2:
    parser.print_help()
    parser.error("incorrect number of arguments")

print(options.name)

# Check attribute is defined
try:
    options.name2
except AttributeError:
    options.name2 = None

if options.name2 is not None :

    print( 'is defined' )
else:
    print( 'not defined' )

if options.name:
    print( 'verbose mode' )

print ( options )
print(options.name)
print(args)

numbers = [1,2,3]
for i in numbers :
    print(i.ob
