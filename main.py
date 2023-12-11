# Crypography Imports
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

# DataBase and Password Maker Imports
import data
import maker

class Encryption:
    def __init__(self) -> None:
        ...

    def encrypt(self, master_password, salt, target_item):
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

    def decrypt(self, master_password, salt, target_item):
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
        except Fernet.InvalidToken: return 1 
        else: return result


class Password_Manger():
    def __init__(self, filename) -> None:
        self.username = None
        self.master_password = None
        self.filename = filename
        self.salt = None
        self.verfied = None

    def register(self, username, master_password):
        # Intialize Values
        self.username = username
        self.master_password = master_password
        self.salt = os.urandom(16)
        encryption = Encryption()

        # Intialize Databbase Instance
        database = data.database()

        # Create Database
        database.create_db(self.filename)

        # Add up the user
        match database.add_user(self.username, self.salt):
            case 1:
                return 1
            
        # Store Auth Record
        auth_pass = Encryption.encrypt(self.master_password,self.salt, "Auth Pass")
        data.add_password(username, "Authentication Record", auth_pass)
        
        # Update Verfication Status
        self.verfied = True

    def login(self, username, master_password):

        # Intilaize Values
        retrived_salt = data.database.retrive_salt(username)
        retrived_auth_pass = data.database.retrive_encrypted_password(username,"Authentication Record")
        result = Encryption.decrypt(master_password,retrived_salt, retrived_auth_pass)
        
        if result != 1:

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
    