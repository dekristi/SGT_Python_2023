from itertools import count

# def prime_num():
#     a=1
#     while True:
#        if a == 1:
#           a += 1
#        else:
#           for c in count(a+1):
#             for i in range(2, c):
#                 if c % i == 0:
#                    break
#                 else:
#                     yield c
#             a += 1

# result = prime_num()

# next(result)

# next(result)

def prime_num():
    a = 0
    while True:
        if a < 2:
            a == 2
        else:
            if all(a%i!=0 for i in range(2,a)):
                yield a   
            a += 1

result = prime_num()

next(result)

next(result)
next(result)
next(result)
next(result)
next(result)