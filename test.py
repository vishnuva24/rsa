from bignum import BigNum, randgen
from rsa_functions import gcd, eegcd, mod_inv, expmod, miller_rabin, primegen, keygen, encrypt, decrypt

def eegcd(a, b): #extended euclid gcd
    r, r1 = a, b
    s, s1 = BigNum(1), BigNum([0])
    t, t1 = BigNum([0]), BigNum(1)
    # assert: r_0, r_1, s_0, s_1, t_0, t_1 are established
    # INV: after i iterations, q_i = r_(i-1)//r_i; s_i = s_(i-1) - q_i*s_(i-2); t_i = t_(i-1) - q_i*t_(i-2); r_i = s_i*a + t_i*b
    #      gcd(a,b) = gcd(r_(i-1), r_i)
    while r1 != BigNum([0]):
        q = r//r1
        s, s1 = s1, s - q*s1
        t, t1 = t1, t - q*t1
        r, r1 = r1, r - q*r1
    # assert: r_0 = gcd(a,b), s_0*a + t_0*b = r_0
    return r, s, t

a = BigNum(243)
b = BigNum(3)
print(eegcd(b,a))