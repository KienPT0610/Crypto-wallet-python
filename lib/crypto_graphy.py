from cryptography.fernet import Fernet

# Tạo khóa bí mật mới để mã hóa và giải mã
def generate_key():
    return Fernet.generate_key()

# Mã hóa văn bản
def encrypt(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

# Giải mã văn bản
def decrypt(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message


