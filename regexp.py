import re
import github3

string = 'ahoj 333'
string = string.replace('hoj', 'pic', 1)
regexp = re.compile('^(\w+) (\d+)')

if re.match(regexp, string):
    match = regexp.search(string)
    print( match.group(1) )

d = 'string'

pole = ['strin', 'string2', 'string3']

b = lambda x: 'beginning_' + x[1:]

mod = map(b, pole)

a = [i for i in mod ]
print(a)

verylongstsring = 'ahojahojahoj'
print(verylongstsring.replace('ah', 'pico', 1))

def walk_users(orgs):

    def out():
        return [1,2,3,4]

    for org in orgs:
        for o in out():
            yield org, o

n = walk_users(['dev', 'hm410'])

for i in n:
    print(i)

import sys
import os
print(os.path.abspath(os.path.dirname(sys.argv[0])))

a=1

if a==1:
    print('je 1')

if hostname != None:
    print('ups')
    print(hostname)