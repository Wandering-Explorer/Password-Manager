# Crypography Imports
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken

# DataBase and Password Maker Imports
import data
import maker

class Encryption:
    def __init__(self) -> None:
        ...

    def encrypt(self, master_password : str, salt : bytes, target_item : bytes):
        password = master_password.encode('utf-8')
        salt = salt
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        return f.encrypt(target_item)

    def decrypt(self, master_password, salt, target_item : bytes):
        password = master_password.encode('utf-8')
        salt = salt
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        try: result = f.decrypt(target_item)
        except InvalidToken: return 1 
        else: return result


class Password_Manger():
    def __init__(self, filename) -> None:
        self.username = None
        self.master_password = None
        self.filename = filename
        self.salt = None
        self.verfied = None
        self.database = data.Database()
        self.encryption = Encryption()

        self.database.create_db(filename) 

    def register(self, username, master_password):
        # Intialize Values
        self.username = username
        self.master_password = master_password
        self.salt = os.urandom(16)

        # Create Database
        self.database.create_db(self.filename)

        # Add up the user
        if self.database.add_user(self.username, self.salt) == 1:
            return 1
            
        # Store Auth Record
        auth_pass = self.encryption.encrypt(self.master_password, self.salt, b"Auth Pass")
        self.database.add_password(username, "Authentication Record", auth_pass)
        
        # Update Verfication Status
        self.verfied = True

    def login(self, username, master_password):

        # Intilaize Values
        retrived_salt = self.database.retrive_salt(username)
        retrived_auth_pass = self.database.retrive_encrypted_password(username,"Authentication Record")[0]
        result = self.encryption.decrypt(master_password, retrived_salt, retrived_auth_pass)
        
        if result != "Auth Pass":

        # Intialize quick  acces values
            self.username = username
            self.master_password = master_password
            self.salt = retrived_salt
            self.verfied = True
            return 0
        
        else:
        # Update quick values
            self.verfied = False
            return 1
        
    def retrive_all_passwords(self, username):
        return self.database.retrive_all_passwords(username)
