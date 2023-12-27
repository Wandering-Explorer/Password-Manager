# GUI imports
import PySimpleGUI as sg

# Password Maker Imports
from maker import make_distinct_password
from password_generator_elements import *
from typing import List

def run_password_generator():
    def make_layout():
        header, main_menu_layout, examples_layout = return_sub_layouts()


        layout = [
            [header],
            [sg.Column(main_menu_layout, visible = True, pad = (0, 5), background_color = 'white', key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-'),
            sg.Column(examples_layout, visible = False, pad = (0, 5), background_color = 'white', key = '-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-')]
        ]
        return layout

    window = sg.Window('Password Generator', make_layout(), background_color = 'white')
    while True:
        event, values = window.read()
        print(f"\n{event}\n{values}")
        if event == sg.WIN_CLOSED or event == 'Cancel': 
            break

        # Switch To Main Layout
        if event == '-PASSWORD-GENERATOR-MAIN-MENU-':
            window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-'].update(visible = False)
            window['-PASSWORD-GENERATOR-MAIN-LAYOUT-'].update(visible = True)

        # Switch To Examples Layout
        if event == '-PASSWORD-GENERATOR-EXAMPLES-MENU-':
            window['-PASSWORD-GENERATOR-MAIN-LAYOUT-'].update(visible = False)
            window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-MULTILINE-'].update('')
            window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-'].update(visible = True)

            # Gather Data
            try:
                password_length = int(values['-PASSWORD-GENERATOR-MAIN-LAYOUT-PASSWORD-LENGTH-'])
            except:
                window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-MULTILINE-'].update("Error: A Length Is Required To Precced")
            else:
                if password_length > 1000:
                    password_length = 1000
                    window['-PASSWORD-GENERATOR-MAIN-LAYOUT-PASSWORD-LENGTH-'].update(1000)
                if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-UPPERCASE-CHARACTERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-LOWERCASE-CHARACTERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-NUMBERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-SPECIAL-CHARACTERS-'] is not True:
                    window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-MULTILINE-'].update("Error: One Of The Checkboxes Must Be Ticked")
                else:
                    # Populate Characterset 
                    character_set = []
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-UPPERCASE-CHARACTERS-'] is True:
                        character_set.append('uppercase_chars')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-LOWERCASE-CHARACTERS-'] is True:
                        character_set.append('lowercase_chars')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-NUMBERS-'] is True:
                        character_set.append('numbers')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-SPECIAL-CHARACTERS-'] is True:
                        character_set.append('special_chars')

                    # Update Progressbar & Get Password Data
                    generated_password_string = ""
                    for i in range(25):
                        genarated_password = f"{make_distinct_password(password_length, character_set)}\n" # Python 3.12 required!
                        generated_password_string += genarated_password
                        window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-PROGRESS-BAR-'].UpdateBar(i + 1)

                    # Show output & Clear Progress Bar
                    generated_password_string = generated_password_string.rstrip()
                    window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-MULTILINE-'].update(generated_password_string)
                    window['-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-PROGRESS-BAR-'].update()

        # Generate Sendable Password
        if event == '-PASSWORD-GENERATOR-MAIN-LAYOUT-SUBMIT-':
            try:
                password_length = int(values['-PASSWORD-GENERATOR-MAIN-LAYOUT-PASSWORD-LENGTH-'])
            except:
                window['-PASSWORD-GENERATOR-MAIN-LAYOUT-ERROR-'].update("Error: A Length Is Required To Precced", visible = True)
            else:
                if password_length > 1000:
                    password_length = 1000
                window['-PASSWORD-GENERATOR-MAIN-LAYOUT-PASSWORD-LENGTH-'].update(1000)
                if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-UPPERCASE-CHARACTERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-LOWERCASE-CHARACTERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-NUMBERS-'] is not True and values['-PASSWORD-GENERATOR-MAIN-LAYOUT-SPECIAL-CHARACTERS-'] is not True:
                    window['-PASSWORD-GENERATOR-MAIN-LAYOUT-ERROR-'].update("Error: One Of The Checkboxes Must Be Ticked", visible = True)
                else:
                    # Populate Characterset 
                    character_set = []
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-UPPERCASE-CHARACTERS-'] is True:
                        character_set.append('uppercase_chars')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-LOWERCASE-CHARACTERS-'] is True:
                        character_set.append('lowercase_chars')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-NUMBERS-'] is True:
                        character_set.append('numbers')
                    if values['-PASSWORD-GENERATOR-MAIN-LAYOUT-SPECIAL-CHARACTERS-'] is True:
                        character_set.append('special_chars')

                    # Generate Password & Inform Status
                    genarated_password = make_distinct_password(password_length, character_set)
                    window.close()
                    return genarated_password

    window.close()
    return None
