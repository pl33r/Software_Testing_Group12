from online_shopping_cart.user.user import User
from online_shopping_cart.user.user_data import UserDataManager
from online_shopping_cart.user.user_interface import UserInterface

###################################
# USER CREDIT CARD DATA FUNCTIONS #
###################################


def change_credit_card_details(user: User) -> None:
    """
    Change the user's credit card details in the file
    """
    data = UserDataManager.load_users()
    for entry in data:
        if entry['username'].lower() == user.name.lower():
            # Iteratively ask the user if they want to add a credit card to their account
            while True:
                card_option: str = UserInterface.get_user_input(
                    prompt="Enter a credit card change option (a to add credit card, r to remove credit card): ").lower()
                if card_option == 'a':
                    number = UserInterface.get_user_input(
                        prompt="Enter the credit card number: ")
                    date_of_expiry = UserInterface.get_user_input(
                        prompt="Enter the date of expiry: ")
                    name = UserInterface.get_user_input(
                        prompt="Enter the name on the credit card: ")
                    cvv = UserInterface.get_user_input(
                        prompt="Enter the CVV on the credit card: ")
                    user.cards.append({"number": number, "date_of_expiry": date_of_expiry, "name": name, "cvv": cvv})
                    print('Successfully added credit card.')
                    break
                elif card_option == 'r':
                    if len(user.cards) > 0:
                        print('\nYour credit cards:')
                        for i, card in enumerate(user.cards):
                            print(f'{i + 1}. {str(card)}')
                        while True:
                            choice: str = UserInterface.get_user_input(prompt='\nEnter the credit card index: ').lower()
                            if choice.isdigit() and 1 <= int(choice) <= len(user.cards):
                                user.cards.pop(int(choice) - 1)
                                print('Successfully removed credit card.')
                                break
                            else:
                                print('Invalid input. Please try again.')
                        break
                    else:
                        print('You have no registered credit card. Please try again!')
                else:
                    print('Invalid input. Please try again.')
            entry['cards'] = user.cards
            UserDataManager.save_users(data=data)
            break