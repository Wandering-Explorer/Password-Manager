# GUI library
import PySimpleGUI as sg

# Password Manager Imports
from main import Password_manager
from maker import make_distinct_password

# GUI imports
from gui_elements import *
from gui_functions import right_click_menu_operations, return_formated_password_data, return_selected_entries, return_formatted_entries_table_data
import password_generator_gui

sg.theme('DarkAmber')

selected_row = None

layout = [
    [
        sg.Column(login_layout, key = '-LOGIN-LAYOUT-', visible = True),
        sg.Column(sign_up, key = '-SIGN-UP-', visible = False),
        sg.Column(all_passwords_layout, key = '-PASSWORD-MANAGER-', visible = False),
        sg.Column(add_password_layout, key = '-ADD-ENTRY-LAYOUT-', visible = False),
        sg.Column(edit_password_layout, key = '-EDIT-ENTRY-LAYOUT-', visible = False), 
    ]
]

window = sg.Window(
    'Password Manager',
    layout,
    margins = (30, 30),
    use_default_focus = True,
    grab_anywhere = True,
    )

while True:
    event, values = window.read()
    print(f"\n{event}\n")
    print(f"\n{values}\n")

    if event in (None, 'Exit'):
        break

    # Intilaize The Selected Row By User In The Main Layout
    if isinstance(event, tuple) == True:
        selected_row = event[2][0]

    # Login Header Navigations 
    if event in ['-SIGN-UP-HEADER-SIGN-UP-BUTTON-', '-LOGIN-HEADER-SIGN-UP-BUTTON-']:
        window['-LOGIN-LAYOUT-'].update(visible = False)
        window['-SIGN-UP-'].update(visible = True)

    # Sign Up Header Navigations 
    if event in ['-SIGN-UP-HEADER-LOGIN_BUTTON-', '-LOGIN-HEADER-LOGIN_BUTTON-']:
        window['-LOGIN-LAYOUT-'].update(visible = True)
        window['-SIGN-UP-'].update(visible = False)
    
    # Sign Up 
    if event == '-SIGN-IN-SUBMIT-':
        username = values['-SIGN-UP-USERNAME-']
        password = values['-SIGN-UP-PASSWORD-']
        confirm_password = values['-SIGN-UP-CONFIRM-PASSWORD-']

        if password != confirm_password:
            window['-SIGN-IN-ERROR-'].update("Passwords Do Not Match", visible = True)
        else:
            window['-SIGN-IN-ERROR-'].update(visible = False)

            if username and password and confirm_password:
                password_manager = Password_manager('pass.db')
                register_return = password_manager.register(username, password)

                # Check For Registration Error (True == Error)
                if isinstance(register_return, str) == True:
                    window['-SIGN-IN-ERROR-'].update(register_return, visible = True)
                else:
                    window['-SIGN-IN-ERROR-'].update(visible = False)

                    # Update entries's Table 
                    password_list = return_formatted_entries_table_data(password_manager)
                    window['-PASSWORD-MANAGER-TABLE-'].update(password_list)

                    # Update Window
                    window['-SIGN-UP-'].update(visible = False)
                    window['-PASSWORD-MANAGER-'].update(visible = True)
            else:
                # If Username & Passwords Are Not Filled:
                window['-SIGN-IN-ERROR-'].update("Username & Passwords Can't Be Left Blank", visible = True)

    # Log In 
    if event == '-LOGIN-SUBMIT-':
        username = values['-LOGIN-USERNAME-']
        password = values['-LOGIN-PASSWORD-']

        password_manager = Password_manager('pass.db')
        if username and password:
            login_return = password_manager.login(username, password)

            match login_return:
                # Return Username Is Not Found
                case 1:
                    window['-LOGIN-ERROR-'].update("Error: Wrong Password --- Try Again", visible = True)

                # Return Wrong Password
                case str(login_return):
                    window['-LOGIN-ERROR-'].update(login_return, visible = True)

                # When The Stuff Is Right:
                case 0:
                    # Update Entries Table & Window
                    passwords = password_manager.retrive_all_encrypted_entries()
                    password_list = return_formatted_entries_table_data(password_manager)

                    window['-LOGIN-LAYOUT-'].update(visible = False)
                    window['-PASSWORD-MANAGER-TABLE-'].update(password_list)
                    window['-PASSWORD-MANAGER-'].update(visible = True)
        
        # If Username And Passwords Are Not Filled In:
        else:
            window['-LOGIN-ERROR-'].update("Username & Passwords Can't Be Left Blank", visible = True)

    # Add Entry {Header}
    if event == '-PASSWORD-MANAGER-ADD-ENTRY-':
        window['-PASSWORD-MANAGER-'].update(visible = False)
        window['-ADD-ENTRY-LAYOUT-'].update(visible = True)

        # Prefill Entry
        password = make_distinct_password(40, ['uppercase_chars', 'lowercase_chars', 'numbers', 'special_chars'])
        window['-ADD-ENTRY-PASSWORD-'].update(password)

    # Add entries Submit
    if event == '-ADD-ENTRY-SUBMIT-':
        # Initialize Values
        title = values['-ADD-ENTRY-TITLE-']
        name = values['-ADD-ENTRY-NAME-']
        password = values['-ADD-ENTRY-PASSWORD-'].encode('utf-8')

        # If variables are EMPTY
        if not name or not password or not title:
            window['-ADD-ENTRY-ERROR-'].update(visible = True)
        else:
            # Add Entry
            result = password_manager.add_entry(title, name, password)

            # Check If The entries Already Exists 
            if result is not None:
                window['-ADD-ENTRY-ERROR-'].update(result, visible = True)
            else:
                # Update Password List And Window
                password_list = return_formatted_entries_table_data(password_manager)

                window['-ADD-ENTRY-ERROR-'].update(visible = False)
                window['-ADD-ENTRY-LAYOUT-'].update(visible = False)
                window['-PASSWORD-MANAGER-TABLE-'].update(password_list)
                window['-PASSWORD-MANAGER-'].update(visible = True)

    # Deal with right_click_menu
    if event in right_click_menu[1]:
        right_click_menu_operations(event, window, '-ProgressBar-', return_formated_password_data(password_manager), selected_row, password_manager)

    # Password generator (Add Entry & Edit Entry Triggers)
    if event in ['-ADD-ENTRY-PASSWORD-GENERATOR-TRIGGER-', '-EDIT-ENTRY-PASSWORD-GENERATOR-TRIGGER-']:
        generated_password = password_generator_gui.run_password_generator()

        if generated_password is not None:
            window['-ADD-ENTRY-PASSWORD-'].update(generated_password)
            window['-EDIT-ENTRY-LAYOUT-'].update(generated_password)

    # Edit Entry Submit
    if event == '-EDIT-ENTRY-SUBMIT-':
        # Initialize Values
        previous_title = password_list[selected_row][0]
        title = values['-EDIT-ENTRY-TITLE-']
        name = values['-EDIT-ENTRY-NAME-']
        password = values['-EDIT-ENTRY-PASSWORD-'].encode('utf-8')

        # If variables are EMPTY
        if not name or not password or not title:
            window['-EDIT-ENTRY-ERROR-'].update("Error: Fields Can't Be Left Empty!", visible = True)
        else:
            # Encrypt Password
            password = password_manager.encrypt_password(password)

            # Add Password
            result = password_manager.modify_entry(previous_title, title, name, password)

            # Check If The User Is Trying To Modify Authentication Record 
            if result is not None:
                window['-EDIT-ENTRY-ERROR-'].update(result, visible = True)
            else:
                window['-EDIT-ENTRY-ERROR-'].update(visible = False)

                # Update Password List And Window
                password_list = return_formatted_entries_table_data(password_manager)

                window['-EDIT-ENTRY-ERROR-'].update(visible = False)
                window['-EDIT-ENTRY-LAYOUT-'].update(visible = False)
                window['-PASSWORD-MANAGER-TABLE-'].update(password_list)
                window['-PASSWORD-MANAGER-'].update(visible = True)
                    
    # Search entriess By title
    if event == '-PASSWORD-MANAGER-FIND-PASSWORD-ENTER-':
        title = values['-PASSWORD-MANAGER-FIND-PASSWORD-']

        # If title is empty
        if not title:
            # Update Password List 
            password_list = return_formatted_entries_table_data(password_manager)
        else:
            # Try checking If Selected entries Exists & If it Does Retrive It
            password_list = return_selected_entries(password_manager, title)
            if type(password_list) is str:
                window['-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-'].update("Error: Title Not Found", visible = True)
        
        # Update The Passwords Table
        window['-PASSWORD-MANAGER-TABLE-'].update(password_list)

