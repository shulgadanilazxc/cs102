from typing import Tuple
import random
def is_prime(n: int) -> bool:
    """
        Tests to see if a number is prime.
        >>> is_prime(2)
        True
        >>> is_prime(11)
        True
        >>> is_prime(8)
        False
        """
    from math import sqrt
    if n > 1:
        for i in range(2,round(sqrt(n))+1):
            if (n%i)==0:
                return False
        return True
    else:
        return False

def gcd(a: int, b: int) -> int:
    """
        Euclid's algorithm for determining the greatest common divisor.
        >>> gcd(12, 15)
        3
        >>> gcd(3, 7)
        1
        """
    if b == 0: return a
    else:
        return gcd(b, a % b)

def multiplicative_inverse(e: int, phi: int) -> int:
    """
       Euclid's extended algorithm for finding the multiplicative
       inverse of two numbers.
       >>> multiplicative_inverse(7, 40)
       23
       """
    x = 0; old_x = 1
    y = 1; old_y = 0
    gcd = phi; old_gcd = e
    while gcd != 0:
        quotient = old_gcd // gcd 
        old_gcd, gcd = gcd, old_gcd - quotient * gcd
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    gcd, x, y = old_gcd, old_x, old_y
    if x < 0:
        x += phi
    return x

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
