from flask import Flask, render_template, request, jsonify, session, send_file
from web3 import Web3
import qrcode
import io
from lib.crypto_graphy import encrypt, decrypt
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_random_secret_key_here'
app.config['DEBUG'] = True
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
            # Uncomment below to actually create an account
            # account = w3.eth.account.create()
            session["isCreated"] = True
            return render_template("index.html")
        
        return render_template("index.html")

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
        recipient_address = request.form.get("recipient_address")
        token_amount = float(request.form.get("token_amount"))
        
        if not Web3.isAddress(recipient_address):
            return jsonify({"message": "Invalid recipient address."}), 400
        
        sender_address = "0xYourSenderAddressHere"  # Replace with actual sender address
        balance = w3.eth.get_balance(sender_address)
        if token_amount > balance:
            return jsonify({"message": "Insufficient balance."}), 400
        
        transaction = {
            'to': recipient_address,
            'value': w3.toWei(token_amount, 'ether'),
            'gas': 2000000,
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': w3.eth.getTransactionCount(sender_address),
            'chainId': 1
        }
        
        private_key = "your_private_key_here"  # Replace with actual private key
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
        
        txn_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        
        txn_hash = txn_hash.hex()
        return jsonify({"message": f"Transaction sent! Hash: {txn_hash}."})
    
    return render_template("send.html")

@app.route('/read_qrcode', methods=['POST'])
def read_qrcode():
    try:

        # Lấy dữ liệu hình ảnh từ request
        data1 = request.data


        # Chuyển đổi dữ liệu hình ảnh từ blob thành mảng NumPy
        image = np.frombuffer(data1, np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)  # Giải mã từ buffer thành ảnh màu

        # Tiền xử lý ảnh - làm sắc nét ảnh bằng Gaussian Blur
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
        # Khởi tạo QRCodeDetector và giải mã QR code
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)  # data dưới dạng string
        print(f'data = {data}')
        if data:
            return jsonify({"qr_data": data})  # Send data of QR code as JSON
        else:
            return jsonify({"qr_data": None})  # no content of QR code
    except Exception as e:
        return jsonify({"error": str(e)})  # receive error id
    
@app.route('/send', methods=['GET'])
def send():
    return render_template('send.html')

if __name__ == '__main__':
    app.run(debug=True)