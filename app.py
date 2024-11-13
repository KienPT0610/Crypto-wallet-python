from flask import Flask, render_template ,request, jsonify, session
from web3 import Web3
from lib.crypto_graphy import encrypt, decrypt

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_here'

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    if session.get("isCreated") == True:
        print("Session is created")
        return render_template("account_login.html")
    else:
        if request.method == "POST":
            wallet_name = request.form.get("walletNameInput")   
            print("Create account name " + wallet_name)
        #     account = w3.eth.account.create()
            session["isCreated"] = True
            render_template("index.html")
        
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)