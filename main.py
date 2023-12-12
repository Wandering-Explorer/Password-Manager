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

# Esstential Imports
from typing import List, Set, Dict, Tuple

class Encryption:
    def __init__(self) -> None:
        ...

    def encrypt(self, master_password : str, salt : bytes, target_item : bytes) -> str:
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

    def decrypt(self, master_password : str, salt : bytes, target_item : bytes) -> str | int:
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


class Password_manager():
    def __init__(self, filename) -> None:
        self.username = None
        self.master_password = None
        self.filename = filename
        self.salt = None
        self.verfied : bool = None
        self.database = data.Database()
        self.encryption = Encryption()

        self.database.create_db(filename) 

    def register(self, username : str, master_password : str) -> None | int:
        # Intialize Values
        self.username = username
        self.master_password = master_password
        self.salt : bytes = os.urandom(16)

        # Create Database
        self.database.create_db(self.filename)

        # Add up the user
        if self.database.add_user(self.username, self.salt) == 1:
            return 1
            
        # Store Auth Record
        auth_pass : bytes = self.encryption.encrypt(self.master_password, self.salt, b"Auth Pass")
        if (result := self.database.add_password(username, "Authentication Record", auth_pass)) != None:
            return 1

        # Update Verfication Status
        self.verfied = True

    def login(self, username : str, master_password : str) -> int:

        # Intilaize Values
        retrived_salt : bytes = self.database.retrive_salt(username)
        retrived_auth_pass : bytes = self.database.retrive_encrypted_password(username,"Authentication Record")
        result : str = self.encryption.decrypt(master_password, retrived_salt, retrived_auth_pass)
        
        if result != "Auth Pass":

        # Intialize quick  acces values
            self.username : str = username
            self.master_password : str = master_password
            self.salt : bytes= retrived_salt
            self.verfied : bool = True
            return 0
        
        else:
        # Update quick values
            self.verfied : bool = False
            return 1
        
    def retrive_all_passwords(self, username : str) -> List[tuple] | int:
        if self.verfied == True: return self.database.retrive_all_passwords(username) 
        else: None
    
    def retrive_selected_password(self, username : str, name : str):
        return self.database.retrive_encrypted_password(username, name) if self.verfied == True else None
    
    def add_password(self, username : str, name : str, encrypted_pass : bytes):
        if self.verfied == True:
            if (error := self.database.add_password(username, name, encrypted_pass)) != None: return error
    