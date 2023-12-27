# why not?
import PySimpleGUI as sg

def return_sub_layouts():
    header = [
        sg.Text('Main Menu', text_color = 'black', justification = 'center', background_color = '#CCCCCC', pad = (0,0), key = '-PASSWORD-GENERATOR-MAIN-MENU-', size = (10, 1), enable_events = True),
        sg.Text('Examples', text_color = 'black', justification = 'center', background_color = '#CCCCCC', pad = (0.5,0), key = '-PASSWORD-GENERATOR-EXAMPLES-MENU-', size = (10, 1), enable_events = True)
    ]

    main_menu_layout = [
        [
            sg.Text('Password Length: ', text_color = 'black', justification = 'center', expand_x = True, background_color = 'white'), 
            sg.Input('40', expand_x = True, justification = 'center', key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-PASSWORD-LENGTH-')
        ],
        [
            sg.Text('Uppercase Characters: ', background_color = 'white', text_color = 'black'),
            sg.Checkbox(text = None, default = True, key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-UPPERCASE-CHARACTERS-', text_color = 'black', background_color = 'white'),
            sg.Text('Lowercase Characters: ', background_color = 'white', text_color = 'black'),
            sg.Checkbox(text = None, default = True, key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-LOWERCASE-CHARACTERS-', text_color = 'black', background_color = 'white')
        ],
        [
            sg.Text('Numbers: ', background_color = 'white', text_color = 'black'),
            sg.Checkbox(text = None, default = True, key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-NUMBERS-', text_color = 'black', background_color = 'white'),
            sg.Text('Special Characters: ', background_color = 'white', text_color = 'black'),
            sg.Checkbox(text = None, default = True, key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-SPECIAL-CHARACTERS-', text_color = 'black', background_color = 'white')
        ],
        [
            sg.Submit(button_color = '#2988ff', font = ("Helvetica", 11, "bold"), key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-SUBMIT-')
        ],
        [
            sg.Text(text = '', background_color = 'white', key = '-PASSWORD-GENERATOR-MAIN-LAYOUT-ERROR-', expand_x = True, justification = 'center', text_color = 'black')
        ]
    ]

    examples_layout = [
        [sg.Text('Generated Passwords: ', text_color = 'black', justification = 'left', expand_x = True, background_color = 'white', pad = (0, 3))],
        [sg.ProgressBar(25, 'h', (20, 20), bar_color = 'green on grey', key = '-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-PROGRESS-BAR-', pad = ((0, 0),(5, 0)))],
        [sg.Multiline(
        default_text = None, 
        disabled = True,
        background_color = 'grey',
        expand_x = True,
        expand_y = True,
        key = '-PASSWORD-GENERATOR-EXAMPLES-LAYOUT-MULTILINE-',
        pad = (0, 3),
        sbar_background_color = '#f2f2f2',
        size = (60, 10)
        )]
    ]

    return header, main_menu_layout, examples_layout

