import sqlite3
import secrets
from typing import List, Tuple

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


    def add_user(self, username : int, salt : bytes) -> int | str:
        MAX_USER : int = 100000

        result : List[tuple] = self.cur.execute("SELECT * FROM user_info WHERE user_name = ?;", (username,))

        if result.fetchone():
            return "User Alreadly Exists"
        else :
            self.cur.execute("INSERT INTO user_info (user_name, salt) VALUES (?,?);", (username, salt))
            self.con.commit()

            table_name = f"user_{secrets.token_hex(64)}"

            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (title TEXT NOT NULL UNIQUE, name TEXT NOT NULL, encrypted_pass BLOB);")
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
            self.cur.execute("INSERT INTO linker (info_ref, pass_ref) VALUES (?,?);", (info_ref, table_name))
            self.con.commit()

            return 0


    def delete_user(self, username : str) -> None | str:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]

            self.cur.execute(f"DROP TABLE {table_ref}")
            self.cur.execute("DELETE FROM linker WHERE pass_ref = ?", table_ref)
            self.con.commit()

    def add_entry(self, username : str, title : str, name : str, encrypted_pass : bytes) -> str | int:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            try:
                self.cur.execute(f"INSERT INTO {table_ref} (title, name, encrypted_pass) VALUES (?,?,?);", (title, name, encrypted_pass))

            except sqlite3.IntegrityError:
                return "Entry Already Exists"

            self.con.commit()

        return 0

    def remove_entry(self, username : str, title : str) -> None | str:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            self.cur.execute(f"DELETE FROM {table_ref} WHERE title = ?;", (title,))
            self.con.commit()

            return None

    def retrive_encrypted_password(self, username : str, title: str) -> bytes | str:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            try:
                result : bytes = self.cur.execute(f"SELECT encrypted_pass FROM {table_ref} WHERE title = ?;", (title,)).fetchone()[0]

            except TypeError:
                return "Password entiry doesn't exist"

            else:
                return result


    def retrive_salt(self, username : str) -> bytes | str:
        try:
            retrived_salt : bytes = self.cur.execute("SELECT salt FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            return retrived_salt

    def retrive_all_entries(self, username : str) -> List[list[str, str, bytes]] | str:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref: str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            data_struct : List[Tuple[str, str, bytes]] = self.cur.execute(f"SELECT * FROM {table_ref};").fetchall()

            # Convert List Of Tuples To List Of Lists
            result : List[List[str]] = []
            for row in data_struct:
                row_data = []
                for entry in row:
                    row_data.append(entry)
                result.append(row_data)

            return result

    def modify_entry(self, username : str, previous_title: str, present_title : str, name : str, encrypted_password : bytes) -> str | None:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]

        except TypeError:
            return "Username Not Found"

        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            try:
                self.cur.execute(f"UPDATE {table_ref} SET (title, name, encrypted_pass) = (?, ?, ?) WHERE title = ?;", (present_title, name, encrypted_password, previous_title))
                self.con.commit()
            except sqlite3.IntegrityError:
                return "Error: Entry With The Same Title Allready Exists"
            else:
                return

    def retrive_selected_entry(self, username : str, title) -> List[list[str, str, bytes]] | str:
        try:
            info_ref : int = self.cur.execute("SELECT pass_ref FROM user_info WHERE user_name = ?;", (username,)).fetchone()[0]
        except TypeError:
            return "Username Not Found"
        else:
            table_ref : str = self.cur.execute("SELECT pass_ref FROM linker WHERE info_ref = ?;", (info_ref,)).fetchone()[0]
            try:
                data_struct : List[Tuple[str, str, bytes]] =  self.cur.execute(f"SELECT * FROM '{table_ref}' WHERE title = ?;", (title,)).fetchall()
            except Exception:
                return "Entry Not Found"
            else:
                # Convert List Of Tuples To List Of Lists
                result = []
                for row in data_struct:
                    row_data = []
                    for entry in row:
                        row_data.append(entry)
                    result.append(row_data)

                return result