'''
@hm410 learning python
'''

import subprocess
import sys
import re
import os

''' External commands:
subprocess.check_call(['git']+cmd)
return subprocess.check_output(['git']+cmd)
'''

def _run(cmd, out, err):
    p = subprocess.Popen(cmd.split(' '), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()

    if p.returncode == 0:
        out[0] = stdout.splitlines()
        return True
    else:
        err[0] = stderr.splitlines()
        return False

def msg_warning(msg=None):
    print('Warning: %s' % msg)

def exit_error(msg=None):
    sys.exit(msg)

out, err = [None], [None]

def run(command):
    return _run(command, out, err)

command = 'dir C:\\'

if run(command):
    print("OK: vystup:")
    for i in out[0]:
        print(i)
else:
    exit_error('pica')

def subd(path, *subdirs):
    return os.path.join(path, *subdirs)

# Variable params
def variable_params(*args):
    for key, value in enumerate(args):
        print(("Variable params: {0}. {1}").format(key, value))

variable_params( 1, 2, 3, 6 )

# Variable params hashed
def variable_params_dict(**kwargs):
    for key, value in kwargs.items():
        print(("{0}. {1}").format(key, value))

variable_params_dict(apple='fruit', banana='zello')

if __name__ == '__main__':
    print('jedu')

ospath = 'dir' + os.sep + 'file'
ospath = os.path.join('dir', 'file')
'''
comment
'''

def _git(cmd):
    return( subprocess.check_output(['git']+cmd)) # ['git'].extend(cmd)

commands='commandz \nnic'
print(commands.splitlines())
lines=_git(['--version', '-a'])
print(lines)

r=re.compile(r'(.* ?)(.*)$')

line='prvni dalse'
regg = re.compile(r'^(.* )(.*)$')
m = regg.search(line)

if m:
    print(m.group(1))
    print(m.group(2))

os.listdir('.')
# substring indexing
strin = 'picavolecavdebcav'
strin=strin[3:]
print("String je to %s" % strin)

#string replace
strin=strin.replace('cav', 'qav', 3)
print(strin)

out=subprocess.check_output(['git', '--version'])
print(out)

import os
print( "env: %s" % os.environ)

d = (i for i in range(4,7))

def yankuje():
    yield (1)
    print(2)
    yield (2)
print('konec\n')

for i in yankuje():
    print(i)

print(os.path.basename('C:\\temp'))
print(os.path.basename('C:\\temp'))

soubor = 'C:\\temp\\1.c'
print(os.path.dirname(soubor))
new = os.path.join(os.path.dirname(soubor), '2.c' )
print(new)

sys.path.insert(0,'libpy')

print('\n'.join(os.environ['PATH'].split(';')))

print( sys.path )
if 'libpy' in sys.path:
    print( 'libpy is there')

dir='C:\\Users'
if( os.path.isdir(dir)):
    print("Directory %s exists" % dir)
else:
    print("Directory does not exist: %s" % dir)

for elem in os.listdir('.'):
    if(os.path.isdir(elem)):
        print( "%s is directory" % elem)
    elif(os.path.isfile(elem)):
        print( "%s is file" % elem)

sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), 'Python-2.7/lib'))

pole = [ 'rp', 'dru']
print(pole)

def f(t=None):
    print(t)

polefci = [ f('nic'), f('neco') ]
polefci[1]

import tarfile
file='N:\\t.txt'

if os.path.isfile(file):
    f = open('N:\\t.txt', 'w')
    f.write('text\n')
    f.write('text2')

    f = open('N:\\t.txt', 'r')
    for fl in f:
        fl = fl.replace('\n', '')
        print("linka: %s" % fl)
else:
    print( "File %s ain't exist" % file)

pole = [1, 3, 4, 6, 3, 3, 8]
pole.insert(2,22)
print(pole.index(3))

hash={}
for i in pole:
    hash[i]=1

for key in sorted(hash.keys()):
    print(key)

k = 1
steps = 0
breaker = False
for i in pole:
    steps+=1
    print("i: %s" % i)
    for j in pole[k:]:
        steps+=1
        if( i == j ):
            print('matched')
            breaker = True
            break
    k+=1
    if( breaker == True):
        break
print( "stesp: %s" % steps)

print("{}".format(sys.path))

hash = {1:'foo', 2:'bar'}

import random

for i in [1,2,3]:
    print(i)
    if( i == 2):
        break
else:
    print('out')

first=[1,2,3]
second=['a','b','c','d']

# enumerate, zip
# insert, remove
# tuples are immutable
# setdefault (in dictionary)


for a,b in zip(first,second):
    print("{} {}".format(a,b))

foo='tsil'
bar=list(foo)

for b in bar:
    print(b)


