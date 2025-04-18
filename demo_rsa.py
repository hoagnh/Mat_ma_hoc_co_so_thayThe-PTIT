import tkinter as tk
from tkinter import scrolledtext
import random
from sympy import isprime, mod_inverse


# RSA Core
def generate_prime(bits=512):
    while True:
        num = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if isprime(num):
            return num

def generate_keys():
    p = generate_prime()
    q = generate_prime()
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


# Giao diện
def process_rsa():
    message = entry_message.get()
    if not message:
        return

    public_key, private_key, p, q, phi, e, d = generate_keys()

    try:
        ciphertext = encrypt(message, public_key)
        decrypted = decrypt(ciphertext, private_key)

        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, f"Đoạn văn bản cần mã hóa: {message}\n")
        text_result.insert(tk.END, f"Số nguyên tố p: {p}\n")
        text_result.insert(tk.END, f"Số nguyên tố q: {q}\n")
        text_result.insert(tk.END, f"Giá trị n (p * q): {p * q}\n")
        text_result.insert(tk.END, f"Giá trị phi(n): {phi}\n")
        text_result.insert(tk.END, f"Giá trị e: {e}\n")
        text_result.insert(tk.END, f"Giá trị d: {d}\n")
        text_result.insert(tk.END, f"Bản mã hóa: {ciphertext}\n")
        text_result.insert(tk.END, f"Bản giải mã: {decrypted}\n")

    except Exception as e:
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, f"Lỗi: {e}")


# UI
root = tk.Tk()
root.title("RSA Demo App Nhom 1")

tk.Label(root, text="Nhập văn bản cần mã hóa:").pack(pady=5)
entry_message = tk.Entry(root, width=60)
entry_message.pack(pady=5)

btn_process = tk.Button(root, text="Mã hóa và Giải mã", command=process_rsa)
btn_process.pack(pady=10)

text_result = scrolledtext.ScrolledText(root, width=90, height=30, wrap=tk.WORD)
text_result.pack(pady=5)

root.mainloop()
