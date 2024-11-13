from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Tạo khóa AES 256 bit và IV 128 bit
key = os.urandom(32)  # Khóa 256 bit
iv = os.urandom(16)   # Vector khởi tạo 128 bit

# Hàm mã hóa
def encrypt(data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data.encode() + b"\0" * (16 - len(data) % 16)  # Padding dữ liệu
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted

# Hàm giải mã
def decrypt(encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.rstrip(b"\0").decode()  # Xóa padding

