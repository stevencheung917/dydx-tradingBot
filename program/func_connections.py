import os
from web3 import Web3
from dydx3 import Client
from decouple import config
from constants import (
    HOST,
    Ethereum_address,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PRIVATE_KEY,
    HTTP_PROVIDER,
      
)

#Connect to DYDX
def connect_dydx():

    
    client=Client(
        host=HOST,
        api_key_credentials={
            "key":DYDX_API_KEY,
            "secret":DYDX_API_SECRET,
            "passphrase":DYDX_API_PASSPHRASE
        },
        stark_private_key=STARK_PRIVATE_KEY,
        eth_private_key=config("ETH_PRIVATE_KEY") ,
        default_ethereum_address=Ethereum_address,
        web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))


    )
    account = client.private.get_account()
    account_id = account.data["account"]["id"]
    account_balance = account.data["account"]["quoteBalance"]
    print("connection successful!")
    print("current balance=",account_balance)
    return client
    