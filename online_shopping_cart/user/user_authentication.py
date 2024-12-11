###############################
# USER AUTHENTICATION CLASSES #
###############################
from online_shopping_cart.user.user_data import UserDataManager


class PasswordValidator:

    @staticmethod
    def is_valid(password) -> bool:
        special_characters = "!@#$%^&*()-+?_=,<>/"
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(c in special_characters for c in password):
            return False
        return True


class UserAuthenticator:

    @staticmethod
    def login(username, password, data) -> dict[str, str | float] | None:
        is_user_registered: bool = False

        for entry in data:
            if entry['username'].lower() == username.lower():
                is_user_registered = True
            if is_user_registered:
                if entry['password'].lower() == password.lower():
                    print('Successfully logged in.')
                    try:
                        cards = entry['cards']
                    except KeyError:
                        cards = list()
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet'],
                        'cards': cards
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, cards, data) -> None:
        new_reg={"username":username,"password":password ,"wallet":0.0, "cards":cards}
        data.append(new_reg)
        UserDataManager.save_users(data)
        print("User registered successfully.")
