import string
import secrets
import csv

# Crypography Imports
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

class Password:
    def __init__(self, alpha, num, special_characters) -> None:
        self.alpha = alpha
        self.num = num
        self.special_characters = special_characters

    def make(self) -> str:
        alpha = self.get_array('alpha', self.alpha)
        num = self.get_array('num',self.num)
        special_characters = self.get_array('s_chars', self.special_characters)

        password = []
        value_list = [alpha, num, special_characters]

        while len(value_list) != 0:
            catagory = value_list[secrets.randbelow(len(value_list))]
            element = catagory[secrets.randbelow(len(catagory))]
            password.append(element)
            catagory.remove(element)
            value_list.remove(catagory) if len(catagory) == 0 else None

        result = ""
        for i in password:
            result += i

        return result
    
    def get_array(self, type, length):
        sequence = ""

        match type:
            case 'alpha':
                sequence = string.ascii_letters
            case 'num':
                sequence = string.digits
            case 's_chars':
                sequence = string.punctuation
        
        result = []

        for i in range(length):
            result.append(secrets.choice(sequence))

        return result

class Storage:
    def __init__(self, path) -> None:
        self.path = path

    def store(self, item):
        with open(self.path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow([item])
    
    def retrive(self): #TODO
        with open(self.path, 'r', newline='') as f:
            reader = csv.reader(f)
            list = []
            for row in reader:
                for item in row:
                    list.append(item)
            return list[0]


class Authentication:
    def __init__(self, master_password) -> None:
        self.master_password = master_password

    def check(self):
        master_password = self.master_password

        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        iterations=500000,
        )

        key = kdf.derive(master_password)

        storage = Storage("Authentication_code.csv")
        stored_key = storage.retrive()

        try:
            kdf.verify(key, stored_key)
        except InvalidKey:
            raise "Authentication_Failure" 
        
    def store(self):
        master_password = self.master_password

        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        iterations=500000,
        )

        key = kdf.derive(master_password)
        storage = Storage("Authentication_code.csv")
        storage.store(key)
    
    
storage = Storage("test.csv")
storage.store("Hi!")
print(storage.retrive())