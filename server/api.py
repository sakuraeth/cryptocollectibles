import os
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()

WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
ABI_PATH = os.getenv('ABI_PATH')

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

with open(ABI_PATH, 'r') as file:
    contract_abi = json.load(file)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def mint_nft(token_uri):
    nonce = web3.eth.getTransactionCount(ACCOUNT_ADDRESS)
    txn_dict = contract.functions.mint(ACCOUNT_ADDRESS, token_uri).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=PRIVATE_KEY)
    txn_receipt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_receipt)

def fetch_nft_data(token_id):
    try:
        token_uri = contract.functions.tokenURI(token_id).call()
        owner = contract.functions.ownerOf(token_id).call()
        return {'token_uri': token_uri, 'owner': owner}
    except Exception as e:
        return {'error': str(e)}

def transfer_nft(token_id, to_address):
    nonce = web3.eth.getTransactionCount(ACCOUNT_ADDRESS)
    txn_dict = contract.functions.transferFrom(ACCOUNT_ADDRESS, to_address, token_id).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=PRIVATE_KEY)
    txn_receipt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_receipt)