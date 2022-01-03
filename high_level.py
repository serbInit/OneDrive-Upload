import pyfile
from cryptography import fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import base64
import os



def encrypt_file(file_path, key):
    og_file = open(file_path, "rb")
    en_file = open(file_path+".jfe", "wb")
    og_size = os.path.getsize(file_path)
    f = fernet.Fernet(key)
    while og_file.tell() < og_size:
        lb = og_file.read(512000)
        lb = f.encrypt(lb)
        en_file.write(lb)

def decrypt_file(file_path, key):
    og_file = open("downloads/"+file_path, "rb")
    en_file = open("downloads/"+file_path+".decrypted", "wb")
    og_size = os.path.getsize("downloads/"+file_path)
    f = fernet.Fernet(key)
    while og_file.tell() < og_size:
        lb = og_file.read(682764)
        lb = f.decrypt(lb)
        en_file.write(lb)

def encrypt_bytes(pBytes):
    pass

def upload_file(file_path, key):
    encrypt_file(file_path,key)
    file_name = os.path.basename(file_path)
    pyfile.upload_file(file_path+".jfe", hashlib.sha256(file_name.encode("utf-8")).hexdigest())

def download_file(file_name, key):
    pyfile.download_file(hashlib.sha256(file_name.encode("utf-8")).hexdigest(), "downloads/" + file_name)
    decrypt_file(file_name,key)


def key_from_hash(password_hash: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return base64.urlsafe_b64encode(kdf.derive(password_hash))

def key_from_password(passw):
    return key_from_hash(hashlib.sha256(passw.encode("utf-8")).digest(), get_salt())

def get_salt():
    f = open("salt", "rb")
    salt = f.read()
    f.close()
    return salt
