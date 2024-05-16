import random
from rsa_functions import gcd, mod_inv, decrypt

# p, q, n, phi_n, e, d =,24436991318977,34055572380119,832215726615760893022218263,832215726615702400458519168,76060994689140911975842253,62114521893687288827788805


def crack(e, n, Cipher):# take d n and cipher later
    p = pollards_rho(n)
    q = n//p
    phi_N = (p-1)*(q-1)
    d = mod_inv(e, phi_N)
    print('priv_key =', (d, n))
    print('Decrypted text:', decrypt(d, n, Cipher))



def pollards_rho(n):
    x = random.randint(1, n-1) # atarting value
    y = x
    c = random.randint(1, n-1) # constant
    d = 1
    g = lambda x: (x**2 + c) % n
    # assert: x, y, c, d, g are established
    # INV: after i iterations, x = g^i(x), y = g^(2i)(y), d = gcd(|x-y|, n)
    while d == 1:
        x = g(x)
        y = g(g(y))
        d = gcd(abs(x-y), n)
    if d == n:
        # assert: faliure, change constant and try again
        return pollards_rho(n)
    # assert: d is a non-trivial factor of n
    return d
    
e = 76060994689140911975842253
n = 832215726615760893022218263
# print(pollards_rho(n))

message = 'Hello World'
Cipher = '77323734602721437154790179 474351195725652548179741842 481418026336658409648606806 481418026336658409648606806 745594398935457163114956154 699524869002908509387414001 817068762785218786586140738 745594398935457163114956154 306080909929086718132670271 481418026336658409648606806 206102553942180323001442482'

crack(e, n, Cipher)