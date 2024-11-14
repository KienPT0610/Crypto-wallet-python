from flask import request, render_template, session
from web3 import Web3
from lib.crypto_graphy import *
from lib.down_json_account import *
from lib.axiosAccount import *

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))

def set_session_account_data(account, balance):
    account_data = {
        "name": session.get("walletName", "Wallet"),
        "address": account.address,
        "balance": balance,
        "private_key": account._private_key.hex()
    }
    session["isLogin"] = True
    session["account_data"] = account_data

def create_account():
    walletNameInput = request.form["walletNameInput"]
    walletPasswordInput = request.form["walletPasswordInput"]

    # Mã hóa mật khẩu ví
    key = generate_key()
    encryptedWalletPassword = encrypt(str(walletPasswordInput), key)

    session["isCreated"] = True
    session["key"] = key
    session["ecryptedWalletPassword"] = encryptedWalletPassword
    session["walletName"] = walletNameInput


    account = w3.eth.account.create()
    set_session_account_data(account, 0)
    session["privateKey"] = encrypt(account._private_key.hex(), key)

    return render_template("index.html", isCreated=session["isCreated"])

def login_account():
    walletPasswordInput = request.form["walletPasswordInput"]
    decryptedWalletPassword = decrypt(session.get("ecryptedWalletPassword"), session.get("key"))

    if str(walletPasswordInput) == str(decryptedWalletPassword):
        print("Login successfully")
        privateKey = decrypt(session.get("privateKey"), session.get("key"))
        account = w3.eth.account.from_key(privateKey)
        balance = getBalance(account=account.address)
        return account, balance
    else:
        return None
    
def login_with_private_key():
    privateKey = request.form.get("walletPrivateKeyInput")
    print("Private key input: ", privateKey)
    account = w3.eth.account.from_key(privateKey)
    balance = getBalance(account=account.address)
    return account, balance


def getBalances(address):
    return getBalance(address)

def getPrivateKey():
    return decrypt(session.get("privateKey"), session.get("key"))

def sendTokens():
    to = request.form.get("address")
    amount = float(request.form.get("amount"))
    amount_ether = w3.to_wei(amount, "ether")
    memo = str(request.form.get("memo"))

    sendToken(to, amount_ether, memo, getPrivateKey())
    print(getPrivateKey())

def getTransactions(address):
    send_transactions = get_send_transactions(address)
    receive_transactions = get_receive_transactions(address)
    return send_transactions, receive_transactions
