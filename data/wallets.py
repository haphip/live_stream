from data.models import Wallet
from data import config


# todo: написать функцию получения кошельков
WALLETS = [
    Wallet(
        address='0x0a555D126E5F8ea6f6648c2FA1A329B07907AB86',
        seed=config.MM_SEED
    ),
    # Wallet(
    #     address=...,
    #     private_key=...
    # ),
    # Wallet(
    #     address=...,
    #     private_key=...
    # ),
]
