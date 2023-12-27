from win32 import win32clipboard
import time
import threading
from typing import List

def copy(item: str, responder : list) -> None:
    # Set format to prevent item storage in clipboard history and cloud
    win32clipboard.OpenClipboard()
    cf = win32clipboard.RegisterClipboardFormat("ExcludeClipboardContentFromMonitorProcessing")
    win32clipboard.SetClipboardData(cf, 'None')

    # Intialize item format 
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, item)
    win32clipboard.CloseClipboard()

    # Modify A value out of the function
    responder[0] = 'Done'

    # Delay 10 seconds
    time.sleep(10)

    # Empty Clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

def right_click_menu_copy(
    window : object, 
    password_list : List[list[str, bytes]], 
    selected_row : int, 
    ProgressBar : object, 
    username : bool = False, 
    password : bool = False
    ):
    # If Password_list and selected _row are fed
    if not password_list or selected_row is None or selected_row > (len(password_list) - 1):
        return "Error: Password_list / Selected_row not given"

    else:
        # Intialize Variables & Set the window to be visible
        if username == True and password == True:
            return "Error: Username & Password is NOT allowed to be true at the same time"
        elif username == True:
            item : str = password_list[selected_row][1]
        elif password == True:
            item : str = password_list[selected_row][2]

        status = [None]
        window[ProgressBar].Update(visible = True)

        # Start Copy
        copy_thread = threading.Thread(target = copy, args = (item, status,))
        copy_thread.start()
        
        # Wait untill copy is done copying
        while status[0] != 'Done':
            ... 

        # If copying done    
        if status[0] == 'Done':
            for i in range(10):
                window[ProgressBar].UpdateBar(i + 1)
                time.sleep(0.9)

            copy_thread.join()
            window[ProgressBar].Update(visible = False)
            