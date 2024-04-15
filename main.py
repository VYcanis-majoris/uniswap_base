from configparser import ConfigParser
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time

# read config file and fetch relevatn data

config = ConfigParser()
config.read('config.ini')

account = config.get('Account_Details', 'account')
private_key  = config.get('Account_Details', 'private_key')
http_rpc_url = config.get('Connection_Details', 'http_rpc_url')
router_address = config.get('Connection_Details', 'router_address')
router_abi = config.get('Connection_Details', 'router_abi')
token_send = config.get('Token_Details', 'token_send')
token_receive = config.get('Token_Details', 'token_receive')

w3 = Web3(Web3.HTTPProvider(http_rpc_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Fetch Data to verify connection to Base Chain

def base_fetch_data():
    print("Latest Block Number:", w3.eth.block_number)
    #print("Block Details:", w3.eth.get_block('latest'))
    accountBalanceWei = w3.eth.get_balance(account)
    print("Account Balance in Ether:", w3.from_wei(accountBalanceWei, 'ether'))
    print("Base Eth Accounts:", w3.eth.accounts)
    print("Base Chain ID:", w3.eth.chain_id)
    
# Swapping Function - to be tested on Mainnet
    
def uniswap_swap_function():
    router_contract    =    w3.eth.contract(router_address, abi=router_abi) 
    nonce              =    w3.eth.get_transaction_count(account)
    
    swap_transaction   =    router_contract.functions.swapExactETHForTokens(
        0,
        [token_send, token_receive],
        account,
        int(time.time()) + (20*60)
    ).build_transaction({
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'from': account,
        'value': w3.to_wei(0.01, 'ether')
    })
    
    #Sign the transaction
    
    signed_transaction  =   w3.eth.account.sign_transaction(swap_transaction, private_key)
    send_transaction    =   w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print("Transaction Hash:", w3.to_hex(send_transaction))
    w3.eth.wait_for_transaction_receipt(send_transaction)
    print("Transaction Receipt:", w3.eth.get_transaction_receipt(send_transaction))
    
if __name__ == "__main__":    
    base_fetch_data()
    uniswap_swap_function()