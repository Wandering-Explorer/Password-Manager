# GUI library
import PySimpleGUI as sg

sg.theme('DarkAmber')

key = "\u1F51"

# Login Layout
login_layout = [
    [
        sg.Button(
            'Login', 
            key = '-LOGIN-HEADER-LOGIN_BUTTON-', 
            auto_size_button = True, 
            expand_x = True), 
        sg.Button(
            'Sign Up', 
            key = '-LOGIN-HEADER-SIGN-UP-BUTTON-', 
            auto_size_button = True, 
            expand_x = True)
    ],
    [
        sg.Text('Username: ', justification = 'center', expand_x = True),
        sg.Input(key = '-LOGIN-USERNAME-', justification = 'center', expand_x = True)
    ],
    [
        sg.Text('Master Password: ', justification = 'center', expand_x = True), 
        sg.Input(key = '-LOGIN-PASSWORD-', justification = 'center', expand_x = True)
    ],
    [
        sg.Text(visible = False, key = '-LOGIN-ERROR-', expand_x = True, justification = 'center')
    ],
    [
        sg.Submit(key = '-LOGIN-SUBMIT-', bind_return_key= True)
    ]
]

# Sign Up Layout
sign_up = [
    [
        sg.Button('Login', key = '-SIGN-UP-HEADER-LOGIN_BUTTON-', expand_x = True),
        sg.Button('Sign Up', key = '-SIGN-UP-HEADER-SIGN-UP-BUTTON-', expand_x = True) 
    ],
    [
        sg.Text('Username: ', justification = 'center', expand_x = True),
        sg.Input(key = '-SIGN-UP-USERNAME-', expand_x = True, justification = 'center')
    ],
    [
        sg.Text('Master Password: ', justification = 'center', expand_x = True), 
        sg.Input(key = '-SIGN-UP-PASSWORD-', justification = 'center', expand_x = True)
    ],
    [
        sg.Text('Confirm Master Password: ', justification = 'center', expand_x = True), 
        sg.Input(key = '-SIGN-UP-CONFIRM-PASSWORD-', justification = 'center', expand_x = True)
    ],
    [
        sg.Text(visible = False, key = '-SIGN-IN-ERROR-', expand_x = True, justification = 'center'),
    ],
    [
        sg.Submit(key = '-SIGN-IN-SUBMIT-'),
    ]
]

# All Passwords Layout
# Values
password_list = []
heading_list = ["title","username","password"]

# Right_Click
right_click_menu = ['',['Copy Username','Copy Password', 'Edit', 'Delete']]
all_passwords_layout = [
    [
        sg.Button('+', key = '-PASSWORD-MANAGER-ADD-ENTRY-', size = (2, 1)),
        sg.Image(source = 'Icons/Search-Icon.png', expand_x = True, expand_y = True, background_color = '#fdcb52'), 
        sg.Input(key = '-PASSWORD-MANAGER-FIND-PASSWORD-', expand_x = True),
        sg.Button('Search', expand_x = True, key = '-PASSWORD-MANAGER-FIND-PASSWORD-ENTER-')
    ],
    [
        sg.Table(
            values = password_list, 
            headings = heading_list, 
            key = "-PASSWORD-MANAGER-TABLE-",
            expand_x = True,
            expand_y = True,
            hide_vertical_scroll = True,
            col_widths = 5,
            justification = 'center',
            right_click_menu = right_click_menu,
            enable_click_events = True)
    ],
    [
        sg.Push('black'),
        sg.ProgressBar(10, 'h', (20, 20), bar_color = 'green on grey', key = '-ProgressBar-', pad = ((0, 0),(5, 0))),
        sg.Push('black')
    ],
    [sg.Text(None, expand_x = True, expand_y = True, justification = 'center', key = '-PASSWORD-MANAGER-ALL-PASSWORDS-ERROR-', visible = False)]
]

# ADD-PASSWORD LAYOUT
add_password_layout = [
    [
        sg.Text("Enter Title: ", expand_x = True, justification = 'center'),
        sg.Input(key='-ADD-ENTRY-TITLE-', expand_x = True, justification = 'center', do_not_clear = False)
    ],
    [
        sg.Text("Enter Username: ", expand_x = True, justification = 'center'),
        sg.Input(key='-ADD-ENTRY-NAME-', expand_x = True, justification = 'center', do_not_clear = False)
    ],
    [
        sg.Text("Enter Password ", expand_x = True, justification = 'center'),
        sg.Input(key = '-ADD-ENTRY-PASSWORD-', expand_x = True, justification = 'center', do_not_clear = False),
        sg.Image("Icons/key.png",
        expand_x = True, 
        expand_y = True, 
        background_color = '#fdcb52', 
        size = (20, 10), enable_events = True, 
        key = '-ADD-ENTRY-PASSWORD-GENERATOR-TRIGGER-')
    ],
    [
        sg.Text("Error: Fields Can't Be Left Empty!", visible = False, key = '-ADD-ENTRY-ERROR-', expand_x = True, justification = 'center')
    ],
    [
        sg.Submit(key = '-ADD-ENTRY-SUBMIT-', bind_return_key = True)
    ]
]

# Edit Password Layout
edit_password_layout = [
    [
        sg.Text("Enter Title: ", expand_x = True, justification = 'center'),
        sg.Input(key='-EDIT-ENTRY-TITLE-', expand_x = True, justification = 'center')
    ],
    [
        sg.Text("Enter name: ", expand_x = True, justification = 'center'),
        sg.Input(key='-EDIT-ENTRY-NAME-', expand_x = True, justification = 'center')
    ],
    [
        sg.Text("Enter Password ", expand_x = True, justification = 'center'),
        sg.Input(key = '-EDIT-ENTRY-PASSWORD-', expand_x = True, justification = 'center'),
        sg.Image("Icons/key.png",
        expand_x = True, 
        expand_y = True, 
        background_color = '#fdcb52', 
        size = (20, 10), enable_events = True, 
        key = '-EDIT-ENTRY-PASSWORD-GENERATOR-TRIGGER-')
    ],
    [
        sg.Text(visible = False, key = '-EDIT-ENTRY-ERROR-', expand_x = True, justification = 'center')
    ],
    [
        sg.Submit(key = '-EDIT-ENTRY-SUBMIT-', bind_return_key = True)
    ]
]