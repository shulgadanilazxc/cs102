def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    alphabet_str = "abcdefghijklmnopqrstuvwxyz"
    alphabet_str = alphabet_str * 2 + (alphabet_str * 2).upper()
    keyword = (keyword*(len(plaintext)//len(keyword))+keyword[:(len(plaintext) % len(keyword))]).lower()
    i = 0
    for letter in plaintext:
        if letter.isalpha():
            ciphertext += alphabet_str[alphabet_str.index(letter) + alphabet_str.index(keyword[i])]
            i += 1
        else:
            ciphertext += letter
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    alphabet_str = "abcdefghijklmnopqrstuvwxyz"
    alphabet_str = alphabet_str * 2 + (alphabet_str * 2).upper()
    keyword = (keyword*(len(ciphertext)//len(keyword))+keyword[:(len(ciphertext) % len(keyword))]).lower()
    i = 0
    for letter in ciphertext:
        if letter.isalpha():
            plaintext += alphabet_str[alphabet_str.rindex(letter) - alphabet_str.index(keyword[i])]
            i += 1
        else:
            plaintext += letter
    return plaintext


