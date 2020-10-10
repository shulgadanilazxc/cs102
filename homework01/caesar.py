def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
	ciphertext = ""
	s = ""
	x = "abcdefghijklmnopqrstuvwxyz"
	x = x*3 + x.upper()*3
	shift %=26
	for a in plaintext:
	    ciphertext += "".join([x[(x).index(a) + 26 - (-shift)]] if a.isalpha() else a)
	return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
	plaintext = ""
	plaintext = encrypt_caesar(ciphertext, shift = -shift)
	return plaintext
