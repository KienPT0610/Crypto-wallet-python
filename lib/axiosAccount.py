from web3 import Web3
import getAbi
abi = getAbi.getAbi()
address = abi['address']
abiContract = abi['abi']
w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))

contract = w3.eth.contract(address=address, abi=abiContract)
def getBalance(account):
    return w3.from_wei(w3.eth.get_balance(account=account), "ether")

def getName():
    return contract.functions.name().call()

def getSymbol():
    return contract.functions.symbol().call()

