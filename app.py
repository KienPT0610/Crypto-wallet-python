from flask import *
from lib.account_wallet import *
from lib.down_json_account import *
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

    if session.get("isCreated") is None:
        session["isCreated"] = False

    if session.get("isCreated") is False:
        if request.method == "POST":
           create_account()
           return download_file(session["walletName"], session["account_data"]["address"], session["account_data"]["private_key"])
        
    # If session is not created
    else:
        if request.method == "POST":
            result = login_account()
            if result is None:
                return render_template("index.html", isCreated=session.get("isCreated"), error="Login Failded")
            else:
                account, balance = result
                set_session_account_data(account, balance)
                return redirect(f"/account/{account.address}")
    return render_template("index.html", isCreated=session["isCreated"])

@app.route("/login-privatekey", methods=["POST"])
def login_private_key():
    result = login_with_private_key()
    if result is None:
        return "Login failed"
    else:
        account, balance = result
        set_session_account_data(account, balance)
        return redirect(f"/account/{account.address}")


@app.route("/account/<address>", methods=["GET"])
def account_detail(address):
    session["account_data"]["balance"] = getBalances(address)
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
    if request.method == "POST":
        sendTokens()  
        return redirect("/account/" + session["account_data"]["address"])
    return render_template("send.html", account_data=session["account_data"])

@app.route("/transactions", methods=["GET"])
def transactions():
    send_transactions, receive_transactions = getTransactions(session["account_data"]["address"])
    return render_template("transactions.html", send_transactions=send_transactions, receive_transactions=receive_transactions)


if __name__ == '__main__':
    app.run(debug=True)
