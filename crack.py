import random
from rsa_functions import gcd, mod_inv, decrypt

#  p, q, n, phi_n, e, d = 2355907087,3368238499,7935256950500342413,7935256944776196828,7308092682596436899,5837948488583764175


def crack(e, n, Cipher):# take d n and cipher later
    p = PollardRho(n)
    q = n//p
    phi_N = (p-1)*(q-1)
    d = mod_inv(e, phi_N)
    print('priv_key =', (d, n))
    print('Decrypted text:', decrypt(d, n, Cipher))



def PollardRho(n):
    # no prime divisor for 1 

    if (n == 1):
        return n
    # even number means one of the divisors is 2 
    if (n % 2 == 0):
        return 2
    
    # we will pick from the range [2, N) 
    x = (random.randint(0, 2) % (n - 2))
    y = x
 
    # the constant in f(x).
    # Algorithm can be re-run with a different c
    # if it throws failure for a composite. 
    c = (random.randint(0, 1) % (n - 1))
 
    # Initialize candidate divisor (or result) 
    d = 1
 
    # until the prime factor isn't obtained.
    # If n is prime, return n 
    while (d == 1):
     
        # Tortoise Move: x(i+1) = f(x(i)) 
        x = (pow(x, 2, n) + c + n)%n
 
        # Hare Move: y(i+1) = f(f(y(i))) 
        y = (pow(y, 2, n) + c + n)%n
        y = (pow(y, 2, n) + c + n)%n
 
        # check gcd of |x-y| and n 
        d = gcd(abs(x - y), n)
 
        # retry if the algorithm fails to find prime factor
        # with chosen x and c 
        if (d == n):
            return PollardRho(n)
     
    return d

e = 330533995785344237723
n = 488218196117411607767
message = 'Hello World'
Cipher = '401133158832796049055 6818767094665954755 296221997294460630074 296221997294460630074 64367670690185027020 52683489144886450861 292266492688205585653 64367670690185027020 241852253927670951629 296221997294460630074 254799922735288436778'

crack(e, n, Cipher)