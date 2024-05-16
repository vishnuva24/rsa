from bignum import BigNum, randgen
from random import randint
import hashlib

def gcd(a, b): # euclid gcd
    # INV: gcd(a,b) = gcd(b, a%b)
    while b != 0:
        a, b = b, a%b
    return a

def eegcd(a, b): #extended euclid gcd
    r, r1 = a, b
    s, s1 = 1, 0
    t, t1 = 0, 1
    # assert: r_0, r_1, s_0, s_1, t_0, t_1 are established
    # INV: after i iterations, q_i = r_(i-1)//r_i; s_i = s_(i-1) - q_i*s_(i-2); t_i = t_(i-1) - q_i*t_(i-2); r_i = s_i*a + t_i*b
    #      gcd(a,b) = gcd(r_(i-1), r_i)
    while r1 != 0:
        q = r//r1
        s, s1 = s1, s - q*s1
        t, t1 = t1, t - q*t1
        r, r1 = r1, r - q*r1
    # assert: r_0 = gcd(a,b), s_0*a + t_0*b = r_0
    return r, s, t

def mod_inv(a, m): # modular inverse
    # bezout coefficients are the modular inverses with respect to the other number.
    x = eegcd(a, m)[1]
    return x%m

def expmod(b, e, m): # modular exponentiation
    def sqr(x):
        return x*x
    if (e == 0):  
        return 1  
    elif (e%2 == 0):
        return sqr(expmod(b,e//2,m)) % m 
    else: 
        return b*sqr(expmod(b,e//2,m)) % m 
    # proved by induction.

def miller_rabin(n, k): # miller rabin primality test
    if n == 2:
        return True
    if n%2 == 0:
        return False

    s, q = 0, n-1
    # INV: (n-1) = q*2^s
    while q%2 == 0:
        s += 1
        q //= 2
    # assert: (n-1) = q*2^s, q is odd   

    # INV: after i iterations, n is prime with probability p^i
    for i in range(k):
        a = randint(1, n-1)
        b = expmod(a, q, n)
        if b == 1 or b == n-1:
            # assert: n is probably prime
            continue

        for j in range(s-1):
            b = (b**2) % n
            if b == 1:
                # assert: n is composite
                return False
            elif b == n-1:
                break
        else:
            # assert: n is composite
            return False
    return True

def primegen(bits):
    # INV: after i iterations, loop ongoing <=> num is composite
    while True:
        num = randint(2**(bits-1), 2**bits-1)
        if miller_rabin(num, 40):
            break
    # assert: num is prime
    return num

def keygen(bits=32): # RSA key generation
    p = primegen(bits)
    q = primegen(bits)
    n = int(BigNum(p)*BigNum(q))
    phi_n = int((BigNum(p)-BigNum(1))*(BigNum(q)-BigNum(1)))
    e = randint(2, phi_n)
    # INV: loop ongoing <=> gcd(e, phi_n) != 1
    while gcd(e, phi_n) != 1:
        e = randint(2, phi_n)
    # assert: gcd(e, phi_n) = 1
    d = mod_inv(e, phi_n)
    return p, q, n, phi_n, e, d

def encrypt(e, N, m):
    cipher = ""
    # INV: after i iterations, cipher = enctrypted(m[0..i-1]) where each character is encrypted using raising the asscii representation of the character to power e mod N
    for x in m:
        letter = ord(x)
        cipher += str(pow(letter, e, N)) + " "
    # assert: cipher = encrypted(m)
    return cipher

def decrypt(d, N, cipher):
    m = ""
    parts = cipher.split()

    for part in parts:
        if part:
            charecter = int(part)
            m += chr(pow(charecter, d, N)) 

    return m
def hash(message, n):
    # hash is essentially a many to one function. getting the hash from message is easy but getting the message from hash is hard.
    # the %n is used to make the hash is within the range of n, which makes things easier
    return str(int(hashlib.sha256(message.encode()).hexdigest(), 16)%n)
def verify_signature(message, signature, e, n):
    if hash(message, n) == decrypt(e, n, signature):
        print("Signature verified!!!!\n")

p, q, n, phi_n, e, d = keygen(32)
print(f'p: {p}\n q: {q}\n n: {n}\n phi_n: {phi_n}\n e: {e}\n d: {d}\n')
message = "yo what thw fcuk is this shit bro"
cipher_text = encrypt(e, n, message)

# idea is to encrypt the hash using the private key, so it can be decrypted using the public key. Upon decrypting the hash, we can verify by applying sha256 on the original message, an confirming if the same hash is generated. Since only I own the private key, and know the message, only I can hash, encode, and send the a valid signature.
signature = encrypt(d, n, hash(message, n))

print("Message:", message, '\n')
print("Cipher text:", cipher_text, '\n')
print("Signature: ", signature)
verify_signature(message, signature, e, n)
print("Decrypted message:", decrypt(d, n, cipher_text))
