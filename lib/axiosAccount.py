from flask import session
from web3 import Web3
from . import getAbi

abi = getAbi.getAbi()
address = abi['address']
abiContract = abi['abi']
w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))

contract = w3.eth.contract(address=address, abi=abiContract)
def getBalance(account):
    return w3.from_wei(contract.functions.balanceOf(account).call(), "ether")

def getName():
    return contract.functions.name().call()

def getSymbol():
    return contract.functions.symbol().call()

def get_send_transactions(address):
    return contract.functions.getSendTransactions(address).call()

def get_receive_transactions(address):
    return contract.functions.getReceiveTransactions(address).call()

def sendToken(to, amount, content, privateKey):
    account = w3.eth.account.from_key(privateKey)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.sendToken(to, amount, content).build_transaction({
        'chainId': 97,
        'gas': 2000000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': nonce,
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)


# print(getBalance("0xBac2B69C092d8F9D5A102D1762a197A90947DCbB"))
# print(get_send_transactions("0xBac2B69C092d8F9D5A102D1762a197A90947DCbB"))