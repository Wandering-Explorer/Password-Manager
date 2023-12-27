import secrets
import string
from typing import List

def make_distinct_password (
    length : int,
    characterset : List[str]
):
    """
    Makes A Password Useing A Single Length Variable and a characterset 
    Acceptable Values of characterset:
    uppercase_chars,
    lowercase_chars,
    numbers,
    special_chars

    If say we were to make a characterset of all values it would be:
    ['uppercase_chars', 'lowercase_chars', 'numbers', 'special_chars']
    The functions outputs a password based on the given length and the charters allowed via provideing them in characterset.
    """
    # Create Another Instance of the list
    characterset_instance = characterset.copy()

    # Randomize List:
    randomized_list = []
    while len(characterset_instance) != 0:
        random_index = secrets.randbelow(len(characterset_instance))
        randomized_list.append(characterset_instance[random_index])
        characterset_instance.remove(characterset_instance[random_index])


    # Intilaize Master String!
    master_string : str = ""
    for i in randomized_list:
        match i:
            case 'uppercase_chars':
                master_string += ''.join(secrets.choice(string.ascii_uppercase) for i in range(len(string.ascii_uppercase)))
                
            case 'lowercase_chars':
                master_string += ''.join(secrets.choice(string.ascii_lowercase) for i in range(len(string.ascii_lowercase)))
            
            case 'numbers':
                master_string += ''.join(secrets.choice(string.digits) for i in range(len(string.digits)))

            case 'special_chars':
                master_string += ''.join(secrets.choice(string.punctuation) for i in range(len(string.punctuation)))

    # Generate Password
    password = ''.join(secrets.choice(master_string) for i in range(length))

    # Return Password 
    return password

