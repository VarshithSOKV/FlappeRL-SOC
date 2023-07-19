import argparse
from pathlib import Path
import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)

p = parser.parse_args()
#print(p.file_path, type(p.file_path), p.file_path.exists())
text = open(p.file_path,'r')

S = int(text.readline().split(' ')[1])
r = int(math.sqrt(S))
A = int(text.readline().split(' ')[1])
P = np.zeros((S,A,S))
R = np.zeros((S,A,S))
V = np.zeros(S)
I = np.zeros(S)
start = int(text.readline().split(' ')[1])
end = np.array(text.readline().split(' ')[1:]).astype(int)

l = text.readline().split(' ')

while(l[0] == "transition"):
    #print(l[1],l[2],l[3],l[4],l[5])
    i = int(l[1])
    j = int(l[2])
    k = int(l[3])

    R[i][j][k] = float(l[4])
    P[i][j][k] = float(l[5])

    l = text.readline().split(' ')

#print(P)
#print(R)

type = 0
if(l[0] == "mdtype"):
    if(l[1] == "continuing"):
        type = 1

gamma = float(text.readline().split(' ')[2])

#print(gamma)

V[end] = 100000

if(end[0] == -1):
    for _ in range(500):
        for i in range(S):
            l = []
            for j in range(A):
                a = 0
                for k in range(S):
                    a += P[i][j][k] * (R[i][j][k] + gamma * V[k])
                l.append(a)
            l = np.array(l)
            V[i] = np.max(l)
            I[i] = int(np.argmax(l))
else:
    for _ in range(30):
        for i in range(S):
            if(i in end):
                continue
            l = []
            for j in range(A):
                a = 0
                for k in range(S):
                    a += P[i][j][k] * (R[i][j][k] + gamma * V[k])
                if( a != 0):
                    l.append(a)
                else:
                    l.append(-111111111)

            l = np.array(l)
            V[i] = np.max(l)
            I[i] = int(np.argmax(l))
# print(V)
# print(np.array(I).reshape((9,9)))
# i = start
# while(i != end):
    
#     l = np.array([V[i-1], V[i+1], V[i-S], V[i+S]])
#     m = np.max(l)

#     if(m == V[i-1]):
#         print("W", end = " ")
#         i = i-1
#     if(m == V[i+1]):
#         print("E", end = " ")
#         i = i+1
#     if(m == V[i-S]):
#         print("N", end = " ")
#         i = i-S
#     if(m == V[i+S]):
#         print("S", end = " ")
#         i = i+S

i = start
while(i != end):
    #print(I[i],i)
    if(I[i] == 0):
        i = i - int(math.sqrt(S))
        print("N",end=" ")
    elif(I[i] == 1):
        i = i + int(math.sqrt(S))
        print("S",end=" ")
    elif(I[i] == 2):
        i = i - 1
        print("W",end=" ")
    elif(I[i] == 3):
        i = i + 1
        print("E",end=" ")

# print(I[end])