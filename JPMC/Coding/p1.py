from itertools import permutations
n = int(input())
l = [int(i) for i in range(1,n+1)]
p = list(permutations(l))

li=[]
for i in p[:fact(len(l)-1)]:
    flag = 0
    for j in range(1,len(i)):
        s = i[j-1] + i[j]
        if not is_prime(s):
            flag=1
            break
    if flag==0:
        li.append(i)
        
print(li)