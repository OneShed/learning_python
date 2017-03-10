'''
@hm410: Learning Python
'''

import subprocess
import sys

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

string = 'stringstr'
pos=string.find('st')
print(pos)

pole = [1, 2, 4,2, 6]
print(pole.index(2))
dict={}
for i in pole:
    dict[i]=1

print(dict)

pole = [2,3,4,3]
dict={}
for i in pole:
    dict[i]=1

poc=1
def factorial(i):
    global poc # MUST BE GLOBAL !!
    if i == 1:
        poc+=1
        print("Pocitadlo: {}".format(poc))
        return 1
    elif i>1:
        poc+=1
        return i * factorial( i - 1)
    else:
        raise(Exception('Nope'))
kloc=1
def fac(x):
    return 1 if x==1 else ''

p = list(enumerate(pole))
print(p)

print(p[0])

try:
    raise( Exception('pica'))

except:
    print('v pici')
    # pass

dict_var = {'key':2}
if 'key' in dict_var.keys():
    print('key')
#->>

# vs (faster)
try:
    print( dict_var['key'])
except KeyError:
    pass
#<<--

import os
obsah = os.listdir('.')

def defined(*args, **kwargs):
    try:
        kwargs['k']
    except KeyError:
        print('someError')
        sys.exit(1)
    return True

if defined(k=3):
    print('Defined')
else:
    print('Undefined')

a = [1,3,4]
b = [2,4,5]

for a,b in zip(a,b):
    print(a,b)

import getpass

#password = getpass.getpass('je')
#print(password)

print(pole)
for i, value in enumerate(pole):
    print(i, value)

print('je')
pole=[1,2]
#print( pole.reverse())

pole=['a', 'bb']
print(''.join(pole))

# PICKLING
import pickle
pickle.dump(pole, open("polep", "wb"))
# read it
pickled = pickle.load(open("polep", "rb"))
print(pickled)
