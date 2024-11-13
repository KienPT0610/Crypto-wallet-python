from flask import Flask, render_template ,request, jsonify, session
from lib.account_wallet import create_account, login_account

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_here'


@app.route("/", methods=["GET", "POST"])
def index():
    # Check if session is created
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
                return render_template("index.html", isCreated=session["isCreated"], error="Login Failded")
            else:
                account, balance = result
                account_data = {
                    "name": session["walletName"],
                    "address": account.address,
                    "balance": balance,
                    "private_key": account._private_key.hex()
                }
                return render_template("account_login.html", account_data=account_data)
            
    return render_template("index.html", isCreated=session["isCreated"])


if __name__ == '__main__':
    app.run(debug=True)