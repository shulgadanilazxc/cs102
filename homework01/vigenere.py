def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    x = "abcdefghijklmnopqrstuvwxyz"
    x = x*2 +(x*2).upper()
    s = ""
    keyword = (keyword*(len(plaintext)//len(keyword))+keyword[:(len(plaintext)%len(keyword))]).lower()
    for i in range(len(plaintext)):
        ciphertext += "".join([x[x.index((plaintext[i])) + x.index(keyword[i])]])
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    x = "abcdefghijklmnopqrstuvwxyz"
    x = x*2 +(x*2).upper()
    s = ""
    keyword = (keyword*(len(ciphertext)//len(keyword))+keyword[:(len(ciphertext)%len(keyword))]).lower()
    for i in range(len(ciphertext)):
        plaintext += "".join([x[x.rindex(ciphertext[i]) - x.index(keyword[i])]]) 
    return plaintext

