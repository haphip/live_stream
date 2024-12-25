class Wallet:
    def __init__(self, address: str, private_key: str = '', seed: str = ''):
        self.address = address
        self.private_key = private_key
        self.seed = seed

    def __str__(self):
        return (f"Wallet("
                f"address='{self.address}', "
                f"private_key='{self.private_key[:3]}***{self.private_key[-3:]}'"
                f")")
