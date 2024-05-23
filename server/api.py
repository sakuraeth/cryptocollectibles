import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import json
import logging
from web3.gas_strategies.time_based import medium_gas_price_strategy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

WEB3_PROVIDER_URI = os.getenv('WEB3_PROVIDER_URI')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
ABI_PATH = os.getenv('ABI_PATH')

web3 = Web3(HTTPProvider(WEB3_PROVIDER_URI))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.setGasPriceStrategy(medium_gas_price_strategy)

with open(ABI_PATH, 'r') as file:
    contract_abi = json.load(file)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def batch_fetch_nft_data(token_ids):
    batch = []
    for token_id in token_ids:
        batch.append(contract.functions.tokenURI(token_id))
        batch.append(contract.functions.ownerOf(token_id))
    
    results = web3.provider.make_batch_request(batch)
    data = []
    for i in range(0, len(results), 2):
        token_uri = results[i]
        owner = results[i+1]
        logging.info(f'Fetched NFT Data for Token ID {token_ids[i//2]}: Token URI - {token_uri}, Owner - {owner}')
        data.append({'token_id': token_ids[i//2], 'token_uri': token_uri, 'owner': owner})
    return data