from typing import Tuple
def is_prime(n: int) -> bool:
    from math import sqrt
    for i in range(2,round(sqrt(n))+1):
        if (n%i)==0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a        
    return(a) 
    pass


def multiplicative_inverse(e: int, phi: int) -> int:
    e%=phi
    for i in range(1, phi):
        if((i * e) % phi) == 1:
            return i
    return 0
    pass


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))