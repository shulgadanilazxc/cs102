import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
	"""
	Encrypts plaintext using a Caesar cipher.
	>>> encrypt_caesar("PYTHON")
	'SBWKRQ'
	>>> encrypt_caesar("python")
	'sbwkrq'
	>>> encrypt_caesar("Python3.6")
	'Sbwkrq3.6'
	>>> encrypt_caesar("")
	''
	"""
	ciphertext = ""
	alphabet_str = "abcdefghijklmnopqrstuvwxyz"
	alphabet_str = alphabet_str*3 + alphabet_str.upper()*3
	shift %=26
	for word in plaintext:
	    ciphertext += "".join([alphabet_str[alphabet_str.index(word) + 26 + shift]] if word.isalpha() else word)
	return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
	"""
	    Decrypts a ciphertext using a Caesar cipher.
	    >>> decrypt_caesar("SBWKRQ")
	    'PYTHON'
	    >>> decrypt_caesar("sbwkrq")
	    'python'
	    >>> decrypt_caesar("Sbwkrq3.6")
	    'Python3.6'
	    >>> decrypt_caesar("")
	    ''
	    """
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
