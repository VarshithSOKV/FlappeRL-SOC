from math import fabs
import numpy as np


def verify(matrix,order):               #for verification that given matrix is markov chain matrix or not
    flag=True
    for i in range(n):
        sum=0
        for j in range(n):
            sum += float(matrix[i][j])
        if(fabs(sum-1)>0.01):
            flag=False

    return flag    

def markovchain(matrix,n,time):         
    l=[1]
    for _ in range(n-1):
        l.append(0)                     #assumed intial condition as S1 at t=0
    #print(l)
    pvector=np.array(l)                 #pvector gives probability of being at every state at given instant i.e., time

    for t in range(time):
        pvector = np.dot(pvector,matrix)        #as pvector at time 't', depends only on pvector at time 't-1' and markov chain matrix
        #print(pvector)
    """By contitional probability and som examples, I have deduced the multiplication of pvector(1xn) and matrix(nxn) to give new pvector"""
    
    return pvector[time-1]


n=5
T=3
l1=[0.2,0.3,0.2,0.2,0.1]
l2=[0.2,0.1,0.1,0.4,0.2]
l3=[0.5,0.2,0.1,0.1,0.1]
l4=[0.1,0.2,0.1,0.2,0.4]
l5=[0.3,0.3,0.1,0.2,0.1]
M=np.array([l1,l2,l3,l4,l5])


flag=verify(M,n)

if(flag==True):
    print(markovchain(M,n,T))