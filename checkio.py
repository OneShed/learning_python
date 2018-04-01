import sys
pole = (2, 4, 5, 6, 3,3)

pole2=[]

uniqe = [ i for i in pole if i not in pole2 pole2.insert(0,i)]
print(uniqe)

sys.exit(0)

k={}
for p in pole:
    if( p in k.keys()):
        print('Not unique:')
        print(p)
    k[p]=1

def min( *args, **kwargs):

    try:
        # defined ?
        if(kwargs['k']):
            print('defined')
    except KeyError:
        print('neexistuje')

    print(len(args))
    for key in kwargs.keys():
        print( kwargs[key])

    key = kwargs.get("key", None)
    return None

k={}
k[3]=4
k[4]=5
min(56, 34,k=38, j=3 )

