################
# USER CLASSES #
################


class User:
    """
    User class to represent user information
    """

    def __init__(self, name, wallet, cards) -> None:
        self.name: str = name
        self.wallet: float = wallet
        self.cards = cards