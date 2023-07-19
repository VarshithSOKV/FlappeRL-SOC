import numpy as np

def policy(Q,start,end):
    S = [start[0],start[1]]
    policy = []
    while(S != end):
        l = Q[S[0]][S[1]]
        action = np.argmax(l)
        k = S[1]

        if(action == 0 or action == 1):
            if(((S[0] > 2 and S[0] < 6) or S[0] == 8) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 5 and S[0] < 8):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1
        elif(action == 2):
            if(((S[0] > 1 and S[0] < 5) or S[0] == 7) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 4 and S[0] < 7):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1
        elif(action == 3):
            if(((S[0] > 3 and S[0] < 7) or S[0] == 9) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 6 and S[0] < 9):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1


        if(action == 0 and k > 0):
            S[1] = k - 1
        elif(action == 1 and k < 6):
            S[1] = k + 1
        elif(action == 2 and S[0] < 9):
            S[0] = S[0] + 1
            S[1] = k
        elif(action == 3 and S[0] > 0):
            S[0] = S[0] - 1
            S[1] = k
        
        policy.append(action)
    return policy

Q = np.zeros((10,7,4))  #7x10 states and 4 actions each

"""0 - up, 1 - down, 2 - right, 3 - left"""

A = np.ones((10,7,4))
for i in range(7):
    A[0][i][3] = 0
    Q[0][i][3] = float('-inf')
    A[9][i][2] = 0
    Q[9][i][2] = float('-inf')

for i in range(10):
    A[i][0][0] = 0
    Q[i][0][0] = float('-inf')
    A[i][6][1] = 0
    Q[i][6][1] = float('-inf')

P = np.zeros((10,7,4))
for i in range(10):
    for j in range(7):
        n = 0
        for k in range(4):
            n = n + A[i][j][k]
        for k in range(4):
            if(A[i][j][k] == 1):
                P[i][j][k] = 1/n

start = [0,3]
end = [7,3]
els = 0.1

for _ in range(8000):
    S = [start[0],start[1]]
    S_prime = [0,0]
    l = []
    for i in range(4):
        if(A[S[0]][S[1]][i] == 1):
            l.append(i)
    p = np.random.random()
    if p < els:
        action = np.random.choice(l,1,0)
    else:
        action = np.argmax(Q[S[0]][S[1]])

    while(S != end):
 
        k = S[1]

        if(action == 0 or action == 1):
            if(((S[0] > 2 and S[0] < 6) or S[0] == 8) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 5 and S[0] < 8):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1
        elif(action == 2):
            if(((S[0] > 1 and S[0] < 5) or S[0] == 7) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 4 and S[0] < 7):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1
        elif(action == 3):
            if(((S[0] > 3 and S[0] < 7) or S[0] == 9) and S[1] > 0):
                k = S[1] - 1
            elif(S[0] > 6 and S[0] < 9):
                if(S[1] > 1):
                    k = S[1] - 2
                elif(S[1] == 1):
                    k = S[1] - 1


        if(action == 0 and k > 0):
            S_prime[1] = k - 1
        elif(action == 1 and k < 6):
            S_prime[1] = k + 1
        elif(action == 2 and S[0] < 9):
            S_prime[0] = S[0] + 1
            S_prime[1] = k
        elif(action == 3 and S[0] > 0):
            S_prime[0] = S[0] - 1
            S_prime[1] = k

        l = []
        for i in range(4):
            if(A[S_prime[0]][S_prime[1]][i] == 1):
                l.append(i)
        p = np.random.random()
        n = len(l)
        if p < els:
            action_prime = np.random.choice(l,1,0)
        else:
            action_prime = np.argmax(Q[S_prime[0]][S_prime[1]])

        expected_value = 0
        for action2 in l:
            if(action2 == action_prime):
                expected_value += (1 - els) * Q[S_prime[0]][S_prime[1]][action2]
            else:
                expected_value += (els/n) * Q[S_prime[0]][S_prime[1]][action2]

        Q[S[0]][S[1]][action] = Q[S[0]][S[1]][action] + 0.5 * (-1 + 0.9 *(expected_value) - Q[S[0]][S[1]][action])
        S[0] = S_prime[0]
        S[1] = S_prime[1]
        action = action_prime

print(policy(Q,start,end))