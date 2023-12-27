import PySimpleGUI as sg
from clipboard_copy import right_click_menu_copy
from typing import List, NoReturn

def return_formated_password_data(password_manager: object) -> List[list[str, str, bytes]]:
    passwords = password_manager.retrive_all_encrypted_entries()

    # Decrypt & Convert Retrived Entries 
    result = []
    for row in passwords:
        row_data = []
        if 'Authentication Record' not in row:
            for entries in row:
                # Check If Item Is A Password Or Not
                if isinstance(entries, bytes) == True:
                    decrypted_password = password_manager.decrypt_password(entries).decode('utf-8')
                    row_data.append(decrypted_password)
                else:
                    row_data.append(entries)

            result.append(row_data)

    return result

def return_formatted_entries_table_data(password_manager: object):
    entries = password_manager.retrive_all_encrypted_entries()

    # Format Retrived entries 
    result = []
    for row in entries:
        row_data = []
        if 'Authentication Record' not in row:
            for entries in row:
                # Check If Item Is A Password Or Not
                if isinstance(entries, bytes):
                    row_data.append('*' * 4)
                else:
                    row_data.append(entries)

            result.append(row_data)

    return result

def return_selected_entries(password_manager: object, title: str):
    entries = password_manager.retrive_selected_entry(title)
    if isinstance(entries, str) is True:
        return entries
    else:
        # Format Retrived Passwords 
        result = []
        for row in entries:
            row_data = []
            if 'Authentication Record' not in row:
                for entries in row:
                    # Check If Item Is A Password Or Not
                    if isinstance(entries, bytes):
                        row_data.append('*' * 4)
                    else:
                        row_data.append(entries)

                result.append(row_data)

        return result


def right_click_menu_operations(
        event: str,
        window: object,
        ProgressBar: object,
        password_list=None,
        selected_row=None,
        password_manager: object = None
):
    match event:
        case 'Copy Username':
            error = right_click_menu_copy(window, password_list, selected_row, ProgressBar, username=True)
            if type(error) is str:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(error, visible=True)
            else:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(visible = False)

        case 'Copy Password':
            error = right_click_menu_copy(window, password_list, selected_row, ProgressBar, password=True)
            if type(error) is str:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(error, visible=True)
            else:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(visible = False)

        case 'Edit':
            # If The User didn't select any rows
            if not password_list or selected_row is None or selected_row > len(password_list):
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update("Error: Password_list / Selected_row not given", visible=True)
            else:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(visible = False)

                # Change Screen
                window['-PASSWORD-MANAGER-'].update(visible=False)
                window['-EDIT-ENTRY-LAYOUT-'].update(visible=True)

                # Recover Info
                retrived_title = password_list[selected_row][0]
                retrived_username = password_list[selected_row][1]
                retrived_password = password_list[selected_row][2]

                # Intialize username, password
                window['-EDIT-ENTRY-TITLE-'].update(retrived_title)
                window['-EDIT-ENTRY-NAME-'].update(retrived_username)
                window['-EDIT-ENTRY-PASSWORD-'].update(retrived_password)
        case 'Delete':
            # Recover Info
            # If Password_list or selected _row are not fed
            if not password_list or selected_row is None or selected_row > (len(password_list) - 1):
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update("Error: Password_list / Selected_row not given", visible=True)

            else:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update(visible = False)
                print(selected_row, password_list)
                username = password_list[selected_row][0]

                password_manager.remove_entry(username)
                password_list = return_formatted_entries_table_data(password_manager)
                window['-PASSWORD-MANAGER-TABLE-'].update(password_list)
        