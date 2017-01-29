n = 5 # Number of images
l = 2 # Number of temporal scales

x = 2
for j in range(l): # Number of temporal scales
    i = 0
    while i < (n//x):
        print('A = ', x*i)
        print('B = ', x*i+x//2)
        print('C = ', x*i+x)
        i += 1
        print('i = ', i)
    x *= 2
