from flask import request, render_template, session
from web3 import Web3
from lib.crypto_graphy import encrypt, decrypt, generate_key

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))


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
    session["privateKey"] = encrypt(account._private_key.hex(), key)

    return render_template("index.html", isCreated=session["isCreated"])

def login_account():
    walletPasswordInput = request.form["walletPasswordInput"]
    decryptedWalletPassword = decrypt(session.get("ecryptedWalletPassword"), session.get("key"))

    if str(walletPasswordInput) == str(decryptedWalletPassword):
        print("Login successfully")
        privateKey = decrypt(session.get("privateKey"), session.get("key"))
        account = w3.eth.account.from_key(privateKey)
        balance = w3.from_wei(w3.eth.get_balance(account=account.address), "ether")
        return account, balance
    else:
        return None
