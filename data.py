import sqlite3
import secrets

class Database:
    def __init__(self) -> None:
        self.con = None
        self.cur = None

    def create_db(self, filename : str):
        con = sqlite3.connect(filename)
        cur = con.cursor()

        self.con = con
        self.cur = cur

        cur.execute("CREATE TABLE IF NOT EXISTS user_info (pass_ref INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL UNIQUE, salt BLOB);")
        cur.execute("CREATE TABLE IF NOT EXISTS linker (info_ref INTEGER, pass_ref TEXT);")

# TESTED : CORRECT
    def add_user(self, username, salt):
        MAX_USER = 100000

        result = self.cur.execute("SELECT * FROM user_info WHERE user_name = ?;", (username,))

        if result.fetchone():
            return 1
        else :
            self.cur.execute("INSERT INTO user_info (user_name, salt) VALUES (?,?);", (username, salt))
            self.con.commit()

            table_name = f"user_{secrets.randbelow(MAX_USER)}"
            
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (name TEXT NOT NULL, encrypted_pass BLOB);")
            info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
            self.cur.execute("INSERT INTO linker (info_ref, pass_ref) VALUES (?,?);", (info_ref, table_name))
            self.con.commit()

            return 0


    def delete_user(self, username):
        info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        table_ref = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
        self.cur.execute(f"DROP TABLE {table_ref}")
        self.cur.execute("DELETE FROM linker WHERE pass_ref = ?", table_ref)
        self.con.commit()

    def count_user(self):
        user_count = self.cur.execute("SELECT COUNT(user_name) FROM user_info").fetchone()[0]
        return user_count

    # Add & Remove Password
    # TESTED : CORRECT    
    def add_password(self, username, name : str, encrypted_pass):
        info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        table_ref = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
        self.cur.execute(f"INSERT INTO {table_ref} (name, encrypted_pass) VALUES (?,?);", (name, encrypted_pass))
        self.con.commit()
 
        return 0

    def remove_password(self, username, name : str):
        info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        table_ref = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
        self.cur.execute(f"DELETE FROM {table_ref} WHERE name = ?;", (name,))
        self.con.commit()

    # Retrive Encrypted Password & Salt And Count

    def retrive_encrypted_password(self, username, name):
        info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        table_ref = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
        result = self.cur.execute(f"SELECT encrypted_pass FROM {table_ref} WHERE name = ?;", (name,)).fetchone()
        return result

    def retrive_salt(self, username):
        retrived_salt = self.cur.execute("SELECT salt FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        return retrived_salt
    
    def count_pass(self, username):
        password_count = self.cur.execute("SELECT COUNT(pass_ref) WHERE user_name = ?;", (username)).fetchone()[0]
        return password_count
    
    def retrive_all_passwords(self, username):
        info_ref = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        table_ref = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
        return self.cur.execute(f"SELECT encrypted_pass FROM {table_ref};").fetchall()
        
