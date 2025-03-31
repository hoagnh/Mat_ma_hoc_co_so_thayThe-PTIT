import random
from sympy import isprime, mod_inverse


def generate_prime(bits=2048):  
    while True:
        num = random.getrandbits(bits) | (1 << (bits - 1)) | 1  
        if isprime(num):
            return num


def generate_keys():
    p = generate_prime(2048)  
    q = generate_prime(2048)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  
    while phi % e == 0:
        e = generate_prime(16) 

    d = mod_inverse(e, phi)  
    return (e, n), (d, n), p, q, phi, e, d


def encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode(), 'big')
    return pow(message_int, e, n)


def decrypt(ciphertext, private_key):
    d, n = private_key
    message_int = pow(ciphertext, d, n)
    return message_int.to_bytes((message_int.bit_length() + 7) // 8, 'big').decode()


# === Chạy demo ===
public_key, private_key, p, q, phi, e, d = generate_keys()
message = input("Nhập đoạn văn bản cần mã hóa: ")
ciphertext = encrypt(message, public_key)
decrypted_message = decrypt(ciphertext, private_key)

print(f"Số nguyên tố p: {p}")
print(f"Số nguyên tố q: {q}")
print(f"Giá trị n (p * q): {p * q}")
print(f"Giá trị phi(n): {phi}")
print(f"Giá trị e: {e}")
print(f"Giá trị d: {d}")
print(f"Bản mã hóa: {ciphertext}")
print(f"Bản giải mã: {decrypted_message}")
