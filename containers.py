### Containers

# list can be soreted
l = [1, 3, 4, 3]
print(type(l))
l[2] = 24
l.append(0)
l.append(0)
l.append(0)
l.remove(0)
print(l)

# set - uniq list
s = {12, 2, 3}
print(type(s))
s.add(1)
s.add(55)
s.add(55)
s.add(2)
s.remove(3)
print(s)
## error no indexing: print(s[2])
## use:
sorted_list = sorted(set(l))

# tuple - immutable
t = (1, 2, 3)
print(type(t))

# dict
d = {'a': 1, 'b': 4}
print(type(d))
for k in d:
    print(k, d[k])


