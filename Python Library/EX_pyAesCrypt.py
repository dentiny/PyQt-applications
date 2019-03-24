import pyAesCrypy;
password="password";
buffer_size=64*1024;
pyAesCrypt.encryptFile("file.txt", "file.txt.aes",password,buffer_size);
pyAesCrypt.decryptFile("file.txt.aes","file.txt",password,buffer_size);
