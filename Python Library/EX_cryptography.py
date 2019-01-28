# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet;

cipher_key=Fernet.generate_key();
cipher=Fernet(cipher_key);
text=b"Hello world";
encrypted_text=cipher.encrypt(text);
decrypted_text=cipher.decrypt(encrypted_text);
