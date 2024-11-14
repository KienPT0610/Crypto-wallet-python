from flask import Flask, render_template ,request, jsonify, session, send_file, redirect
from lib.account_wallet import create_account, login_account
import os
import qrcode
import io
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545/'))


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Dữ liệu phiên khi vào trang:", session)
    # Check if session is created
    if session is None:
        session.clear()

    if session.get("isCreated") is None:
        session["isCreated"] = False

    if session.get("isCreated") is False:
        if request.method == "POST":
           create_account()
        
    # If session is not created
    else:
        if request.method == "POST":
            result = login_account()
            if result is None:
                return render_template("index.html", isCreated=session.get("isCreated"), error="Login Failded")
            else:
                account, balance = result
                account_data = {
                    "name": session["walletName"],
                    "address": account.address,
                    "balance": balance,
                    "private_key": account._private_key.hex()
                }
                session["isLogin"] = True
                session["account_data"] = account_data
                return redirect(f"/account/{account.address}")
    return render_template("index.html", isCreated=session["isCreated"])


@app.route("/account/<address>", methods=["GET"])
def account_detail(address):
    return render_template("account_login.html", account_data=session["account_data"])


@app.route("/receive", methods=["GET"])
def receive_qr():
    wallet_address = "0xYourWalletAddressHere"  # Replace with actual wallet address
    qr_img = qrcode.make(wallet_address)

    qr_io = io.BytesIO()
    qr_img.save(qr_io, 'PNG')
    qr_io.seek(0)

    return send_file(qr_io, mimetype='image/png')

@app.route("/receive", methods=["POST"])
def create_request():
    data = request.get_json()
    recipient_address = data.get("recipient_address")
    token_amount = data.get("token_amount")
    
    if not recipient_address or not token_amount:
        return jsonify({"message": "Recipient address and token amount are required."}), 400

    response_message = f"Request created for {token_amount} tokens to be sent to {recipient_address}."
    
    return jsonify({"message": response_message})

@app.route("/send", methods=["GET", "POST"])
def send_tokens():    
    return render_template("send.html", account_data=session["account_data"])

if __name__ == '__main__':
    app.run(debug=True)
