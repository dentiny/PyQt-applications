# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet;

cipher_key=Fernet.generate_key();
print(cipher_key);
cipher=Fernet(cipher_key);
text=b"Hello world";
encrypted_text=cipher.encrypt(text);
print(encrypted_text);
decrypted_text=cipher.decrypt(encrypted_text);
print(decrypted_text);