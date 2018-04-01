import re
import github3

string = 'ahoj 333'
string = string.replace('hoj', 'pic', 1)
regexp = re.compile('^(\w+) (\d+)')

if re.match(regexp, string):
    match = regexp.search(string)
    print( match.group(1) )

x = 1
b = lambda x: (x + 1)*3

print(b(3))
