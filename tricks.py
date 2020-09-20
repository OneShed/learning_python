foo = [1,2,3,2,1,3, 3]
s = set(foo)

# find most numerous value
test = [1, 2, 3, 4, 2, 2, 3, 1, 4, 4, 4]
print(max(set(test), key = test.count))
print(max(test, key = lambda test:int(test)))

# unpacking list of variable length
*trailing, lsst_one = [10, 8, 7, 1, 9, 5, 10, 3]

>>> 'Hello'.center(20, '=')
'=======Hello========'


