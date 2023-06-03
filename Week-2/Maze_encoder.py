import argparse
from pathlib import Path
import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument("file_path", type=Path)

p = parser.parse_args()
#print(p.file_path, type(p.file_path), p.file_path.exists())
text = open(p.file_path,'r')
k = len(text.readlines())
text = open(p.file_path,'r')

data =[]

for _ in range(k):
    data.append(list(np.array(text.readline().split(" ")).astype(int)))
data = np.array(data)
#print(data)

S = (k-2)**2
print("numStates",S)
print("numActions",4)

x = np.where(data == 2)[0][0]
y = np.where(data == 2)[1][0]
s = (k-2)*(x-1) + (y-1)

data[x][y] = 0
#print(data)

print("start",s)

x = np.where(data == 3)[0][0]
y = np.where(data == 3)[1][0]
e = (k-2)*(x-1) + (y-1)

data[x][y] = 0
#print(data[5][4],data[5][5])

print("end",e)

for i in range(k-2):
    for j in range(k-2):
        flag1 = flag2 = flag3 = flag4 = 0
        if(data[i][j+1] == 0 and data[i+1][j+1] != 1):
            flag1 = 1
            
        if(data[i+2][j+1] == 0 and data[i+1][j+1] != 1):
            flag2 = 1
            
        if(data[i+1][j] == 0 and data[i+1][j+1] != 1):
            flag3 = 1
            
        if(data[i+1][j+2] == 0 and data[i+1][j+1] != 1):
            flag4 = 1

        # if(i == 5 and j == 4):  
        #     print(flag4)
        #     print(data[i+1][j+1],data[i+1][j+2])
        if(flag1):
            print("transition", (k-2)*(i)+(j), 0, (k-2)*(i-1)+(j), -1, 1)
        if(flag2):
            print("transition", (k-2)*(i)+(j), 1, (k-2)*(i+1)+(j), -1, 1)
        if(flag3):
            print("transition", (k-2)*(i)+(j), 2, (k-2)*(i)+(j-1), -1, 1)
        if(flag4):
            print("transition", (k-2)*(i)+(j), 3, (k-2)*(i)+(j+1), -1, 1)

print("mdtype episodic")
print("discount  1")