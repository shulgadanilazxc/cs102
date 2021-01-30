def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    i = 0
    k = len(keyword)
    for c in plaintext:
        if c.isupper():
            indx = ord(c) - ord("A")
            shift = ord(keyword[i % k]) - ord("A")
            shifted_c = (indx + shift) % 26 + ord("A")
            c_new = chr(shifted_c)
            ciphertext += c_new
        elif c.islower():
            indx = ord(c) - ord("a")
            shift = ord(keyword[i % k]) - ord("a")
            shifted_c = (indx + shift) % 26 + ord("a")
            c_new = chr(shifted_c)
            ciphertext += c_new
        else:
            ciphertext += c
        i += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a  Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    i = 0
    k = len(keyword)
    for c in ciphertext:
        if c.isupper():
            indx = ord(c) - ord("A")
            shift = ord(keyword[i % k]) - ord("A")
            shifted_c = (indx - shift) % 26 + ord("A")
            c_last = chr(shifted_c)
            plaintext += c_last
        elif c.islower():
            indx = ord(c) - ord("a")
            shift = ord(keyword[i % k]) - ord("a")
            shifted_c = (indx - shift) % 26 + ord("a")
            c_last = chr(shifted_c)
            plaintext += c_last
        else:
            plaintext += c
        i += 1
    return plaintext
