'''from bignum import BigNum, randgen
from rsa_functions import gcd, eegcd, mod_inv, expmod, miller_rabin, primegen, keygen, encrypt, decrypt

def miller_rabin(n, k): # miller rabin primality test
    if n == BigNum(2):
        return True
    if n%BigNum(2) == BigNum(0):
        return False

    s, q = BigNum(0), n-BigNum(1)
    
    while q%BigNum(2) == BigNum(0):
        s = s+BigNum(1)
        q = q//BigNum(2)
    print(s.list, q.list, (q%BigNum(2)).list)
    

print(mod_inv(17, 7))'''

grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
def numIslands(grid: list[list[str]]) -> int:
        def DFS(grid, i:int, j:int):
            if (
                i < 0
                or j < 0
                or i >= len(grid)
                or j >= len(grid[0])
                or grid[i][j] != "1"
            ):
                return
            grid[i][j] = "V"
            DFS(grid, i - 1, j)
            DFS(grid, i + 1, j)
            DFS(grid, i, j + 1)
            DFS(grid, i, j - 1)

        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "1":
                    DFS(grid, i, j)
                    count += 1
        return count

# count number of decimal strings of length n that do not contain 2 consecutive prime numbers
def is_prime(n):
    return n in [2, 3, 5, 7]
def valid(k, i, j):
    if is_prime(i) and is_prime(j):
        return False
    if is_prime(k) and is_prime(i):
        return False
    return True
count = 0
for k in range(10):
    for i in range(10):
        for j in range(10):
            if valid(k, i, j):
                count += 1
print(count)