# Design 
The Password Manager features symmetric encryption with fernet. The User's Master Password gets hashed, and then passed onto base64 to encode it in the URL; then, it derives the key from the result. The key is used to encrypt an authentication record and store it in the database. When the user logs in the same stuff happen except; now it tries to decrypt that authentication record using the key and if fails it throws an error at the user. This way only the right user can open the database; as even if someone gets a hold of the database they would need the master password to unlock it.

The Database is designed with a users table and each user has their table for passwords. Titles are unqiue --- for easeing up the searching proces:
![An Image of the database](https://github.com/Wandering-Explorer/password_manager/assets/102423760/62445458-1374-45c2-ac2e-c1ff6585973e)

When the user copies the username or password a timer starts and Windows is notified to prevent all copied text being included in the clipboard history or synchronized to the user's other devices. Keepass's Dev helped me a lot to implement the feature as I am an idiot[^1].

# Instalation 
Installation is simple: just download the repo, install listed librarys and you are done. Whenever you want to open the password manager just run the `gui.py` file.
Dependences:
- PySimpleGUI
- Cryptography
  
# Known Bugs
- When You Try to Copy something useing the right click menu and after the operation you try to do it again it will kinda work but the progress bar would be in left instead of being in the middle

I am looking forward to finding a fix for it 

### references
[^1]: https://sourceforge.net/p/keepass/discussion/329221/thread/565087de57/?limit=25#341a

## License
This project, Password-Manager, © 2023 by Ramanuj Ghosal, is licensed under CC BY-NC 4.0.

You are free to use, share, and adapt the material for non-commercial purposes. Commercial use requires a separate agreement.

This project includes the following third-party libraries:
- **PySimpleGUI**: Licensed under its own terms. See: https://PySimpleGUI.com/eula
- **cryptography**: Licensed under the Apache License 2.0. See: https://www.apache.org/licenses/LICENSE-2.0

Make sure to comply with the licenses of these libraries when using the project.

