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
WALLET_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
ABI_FILE_PATH = os.getenv('ABI_PATH')

web3 = Web3(HTTPProvider(WEB3_PROVIDER_URI))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
web3.eth.setGasPriceStrategy(medium_gas_price_strategy)

with open(ABI_FILE_PATH, 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_instance = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

def fetch_nft_data_in_batches(token_ids):
    call_batch = []
    for token_id in token_ids:
        call_batch.append(contract_instance.functions.tokenURI(token_id))
        call_batch.append(contract_instance.functions.ownerOf(token_id))
    
    results = web3.provider.make_batch_request(call_batch)
    nft_data_list = []
    for i in range(0, len(results), 2):
        token_uri = results[i]
        owner_address = results[i + 1]
        logging.info(f'Fetched NFT Data for Token ID {token_ids[i // 2]}: Token URI - {token_uri}, Owner - {owner_address}')
        nft_data_list.append({'token_id': token_ids[i // 2], 'token_uri': token_uri, 'owner': owner_address})
    return nft_data_list