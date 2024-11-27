from online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from online_shopping_cart.user.user_interface import UserInterface
from online_shopping_cart.user.user_data import UserDataManager
########################
# USER LOGIN FUNCTIONS #
########################


#everything new in this file was done by Julius Amorim according to the instructions given in the assignment 1 task 1

def is_quit(input_argument: str) -> bool:
    return input_argument.lower() == 'q'

def login() -> dict[str, str | float] | None:
    username: str = UserInterface.get_user_input(prompt="Enter your username (or 'q' to quit): ")
    if is_quit(input_argument=username):
        exit(0)  # The user has quit

    password: str = UserInterface.get_user_input(prompt="Enter your password (or 'q' to quit): ")
    if is_quit(input_argument=password):
        exit(0)   # The user has quit

    is_authentic_user: dict[str, str | float] = UserAuthenticator().login(
        username=username,
        password=password,
        data=UserDataManager.load_users()
    )
    if is_authentic_user is not None:
        return is_authentic_user
    
    while True:
        register_option: str = UserInterface.get_user_input(prompt="Would you like to register ('yes' or 'no' or 'q' to quit): ").lower()
        if is_quit(input_argument=register_option):
            exit(0)  
        elif register_option == 'yes':
            password = UserInterface.get_user_input(prompt="Create a password (at least 8 characters, 1 uppercase, 1 special): ")
            while not PasswordValidator.is_valid(password):
                print("Password does not meet the criteria. Try again.")
                password = UserInterface.get_user_input(prompt="Create a password (at least 8 characters, 1 uppercase, 1 special): ")
            UserAuthenticator.register(username, password, UserDataManager.load_users())
            break
        elif register_option == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes,' 'no,' or 'q'.")
    return None
