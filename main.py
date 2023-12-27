# Cryptography Imports
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken

# DataBase and Password Maker Imports
import data

# Essential Imports
from typing import List, Set, Dict, Tuple


class Encryption:
    def __init__(self) -> None:
        ...

    def encrypt(self, master_password: str, salt: bytes, target_item: bytes) -> bytes:
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

    def decrypt(self, master_password: str, salt: bytes, target_item: bytes) -> str | int:
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
        try:
            result = f.decrypt(target_item)
        except InvalidToken:
            return 1
        else:
            return result


class Password_manager():
    def __init__(self, filename) -> None:
        self.username = None
        self.master_password = None
        self.filename = filename
        self.salt = None
        self.verfied: bool = None
        self.database = data.Database()
        self.encryption = Encryption()
        self.database.create_db(self.filename)

    def register(self, username: str, master_password: str) -> None | str:
        """
        Given Username & Master Password; Derives a symmetric encryption key and uses that to store authentication record; 
        Which can only be decrypted useing the same password and salt.  
        """
        self.username = username
        self.master_password = master_password
        self.salt: bytes = os.urandom(16)

        # Add up the user
        return_value = self.database.add_user(self.username, self.salt)
        if isinstance(return_value, str) == True:
            return return_value

        # Store Auth Record
        auth_pass: bytes = self.encryption.encrypt(self.master_password, self.salt, b"Auth Pass")
        self.database.add_entry(self.username, "Authentication Record", "", auth_pass)

        # Update Verfication Status
        self.verfied = True

    def login(self, username: str, master_password: str) -> int | str:
        """
        Given A Username & Master Password Search For Authenctication Records Stored In The Databases Useing Those 
        And Decrypt Them Useing The Master Password; verifing the user on the way. Else Yell at the User For Provideing Incorrect Info
        """
        self.database.create_db(self.filename)
        retrived_salt: bytes = self.database.retrive_salt(username)
        retrived_auth_pass: bytes = self.database.retrive_encrypted_password(username, "Authentication Record")

        # Check If User Alrealdy Exists 
        if type(retrived_salt) == str:
            self.verfied = False
            return retrived_salt

        result: str = self.encryption.decrypt(master_password, retrived_salt, retrived_auth_pass)
        match result:
            # If it's The Pre-fed Password
            case b"Auth Pass":
                self.verfied: bool = True
                self.username: str = username
                self.master_password: str = master_password
                self.salt: bytes = retrived_salt
                self.verfied: bool = True
                return 0

            case 1:
                self.verfied: bool = False
                return "Invalid Password --- Try Again"

    def retrive_all_encrypted_entries(self) -> List[List[str]] | int:
        if self.verfied is True:
            return self.database.retrive_all_entries(self.username)
        else:
            return None

    def retrive_selected_entry(self, title: str) -> List[list[str, str, bytes]] | str | None:
        if self.verfied == True:
            return self.database.retrive_selected_entry(self.username, title)
        else:
            return None

    def add_entry(self, title: str, name: str, password: bytes) -> None | str:
        if self.verfied == True:
            encrypted_password = self.encryption.encrypt(self.master_password, self.salt, password)
            error = self.database.add_entry(self.username, title, name, encrypted_password)
            if error != 0:
                return error
            else:
                return None

    def decrypt_password(self, encrypted_password: bytes):
        decrypted_password = self.encryption.decrypt(self.master_password, self.salt, encrypted_password)
        if decrypted_password != 1:
            return decrypted_password
        else:
            return 1

    def encrypt_password(self, password: bytes) -> bytes:
        encrypted_password = self.encryption.encrypt(self.master_password, self.salt, password)
        if encrypted_password != 1:
            return encrypted_password
        else:
            return 1

    def remove_entry(self, title: str) -> None | str:
        if self.verfied == True:
            return_value = self.database.remove_entry(self.username, title)
            if return_value is not None:
                return return_value
            else:
                return None

    def modify_entry(self, previous_title: str, present_title : str, username: str, password: bytes):
        if present_title == "Authentication Record" or previous_title == "Authentication Record":
            return "Unable To Modify Authentication Record"
        else:
            return self.database.modify_entry(self.username, previous_title, present_title, username, password)
 