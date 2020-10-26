import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
	ciphertext = ""
	alphabet_str = "abcdefghijklmnopqrstuvwxyz"
	alphabet_str = alphabet_str*3 + alphabet_str.upper()*3
	shift %=26
	for word in plaintext:
	    ciphertext += "".join([alphabet_str[alphabet_str.index(word) + 26 + shift]] if word.isalpha() else word)
	return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
	plaintext = ""
	alphabet_str = "abcdefghijklmnopqrstuvwxyz"
	alphabet_str = alphabet_str*3 + alphabet_str.upper()*3
	shift %=26
	for word in ciphertext:
	    plaintext += "".join([alphabet_str[alphabet_str.index(word) + 26 - shift]] if word.isalpha() else word)
	return plaintext

def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    words = ciphertext.split()
    for word in words:
        for i in range(0,26):
            decr_word=decrypt_caesar(word, i)
            if decr_word in dictionary:
                best_shift=i
    return best_shift
