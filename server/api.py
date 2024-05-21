import os
from web3 import Web3
from dotenv import load_dotenv
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        nonce = web3.eth.getTransactionCount(ACCOUNT_ADDRESS)
        txn_dict = contract.functions.mint(ACCOUNT_ADDRESS, token_uri).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=PRIVATE_KEY)
        txn_receipt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt_hex = web3.toHex(txn_receipt)
        logging.info(f'NFT Minted Successfully: {txn_receipt_hex}')
        return txn_receipt_hex
    except Exception as e:
        logging.error(f'Error minting NFT: {str(e)}')
        return {'error': str(e)}

def fetch_nft_data(token_id):
    try:
        token_uri = contract.functions.tokenURI(token_id).call()
        owner = contract.functions.ownerOf(token_id).call()
        logging.info(f'Fetched NFT Data for Token ID {token_id}: Token URI - {token_uri}, Owner - {owner}')
        return {'token_uri': token_uri, 'owner': owner}
    except Exception as e:
        logging.error(f'Error fetching NFT data for Token ID {token_id}: {str(e)}')
        return {'error': str(e)}

def transfer_nft(token_id, to_address):
    try:
        nonce = web3.eth.getTransactionCount(ACCOUNT_ADDRESS)
        txn_dict = contract.functions.transferFrom(ACCOUNT_ADDRESS, to_address, token_id).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=PRIVATE_KEY)
        txn_receipt = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        txn_receipt_hex = web3.toHex(txn_receipt)
        logging.info(f'NFT Transferred Successfully: Token ID {token_id} to {to_address}. Transaction: {txn_receipt_hex}')
        return txn_receipt_hex
    except Exception as e:
        logging.error(f'Error transferring NFT Token ID {token_id} to {to_address}: {str(e)}')
        return {'error': str(e)}