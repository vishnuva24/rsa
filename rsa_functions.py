from random import randint

def gcd(a, b): # euclid gcd
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

def miller_rabin(n, k): # miller rabin primality test
    if n == 2:
        return True
    if n%2 == 0:
        return False

    s, q = 0, n-1
    while q%2 == 0:
        s += 1
        q //= 2
    for i in range(k):
        a = randint(1, n-1)
        b = expmod(a, q, n)
        if b == 1 or b == n-1:
            continue
        for j in range(s-1):
            b = (b**2) % n
            if b == 1:
                return False
            elif b == n-1:
                break
        else:
            return False
    return True

def primegen(bits):
    while True:
        num = randint(2**(bits-1), 2**bits-1)
        if miller_rabin(num, 130):
            break
    return num

def keygen(bits=32): # RSA key generation
    p = primegen(bits)
    q = primegen(bits)
    n = p*q
    phi_n = (p-1)*(q-1)
    e = randint(2, phi_n)
    while gcd(e, phi_n) != 1:
        e = randint(2, phi_n)
    d = mod_inv(e, phi_n)
    return p, q, n, phi_n, e, d

def encrypt(e, N, m):
    cipher = ""

    for x in m:
        msg = ord(x)
        cipher += str(pow(msg, e, N)) + " "

    return cipher

def decrypt(d, N, cipher):
    m = ""

    parts = cipher.split()
    for part in parts:
        if part:
            c = int(part)
            m += chr(pow(c, d, N)) 

    return m


# p, q, n, phi_n, e, d = keygen(32)
# print(f'p: {p}\nq: {q}\nn: {n}\nphi_n: {phi_n}\ne: {e}\nd: {d}')
# message = "Hello World"
# print("Message:", message)
# cipher_text = encrypt(e, n, message)
# print("Cipher text:", cipher_text)
# print("Decrypted message:", decrypt(d, n, cipher_text))


# contains functions: gcd, eegcd, mod_inv, expmod, miller_rabin, primegen, keygen, encrypt, decrypt



