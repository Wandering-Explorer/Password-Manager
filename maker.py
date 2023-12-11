import secrets
import string

class Password:
    def __init__(self, alpha, num, special_characters) -> None:
        self.alpha = alpha
        self.num = num
        self.special_characters = special_characters

    def make(self) -> str:
        alpha = self.get_array('alpha', self.alpha)
        num = self.get_array('num',self.num)
        special_characters = self.get_array('s_chars', self.special_characters)

        password = []
        value_list = [alpha, num, special_characters]

        while len(value_list) != 0:
            catagory = value_list[secrets.randbelow(len(value_list))]
            element = catagory[secrets.randbelow(len(catagory))]
            password.append(element)
            catagory.remove(element)
            value_list.remove(catagory) if len(catagory) == 0 else None

        result = ""
        for i in password:
            result += i

        return result
    
    def get_array(self, type, length):
        sequence = ""

        match type:
            case 'alpha':
                sequence = string.ascii_letters
            case 'num':
                sequence = string.digits
            case 's_chars':
                sequence = string.punctuation
        
        result = []

        for i in range(length):
            result.append(secrets.choice(sequence))

        return result