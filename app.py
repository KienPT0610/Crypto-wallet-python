from flask import Flask, render_template, redirect, url_for
from web3 import Web3

app = Flask(__name__)

# Kết nối với blockchain Binance Smart Chain
web3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))

# Trang chủ: Hiển thị form để tạo ví
@app.route('/')
def index():
    return render_template('index.html', name='', address='', balance='')

# Trang tạo ví: Tạo ví mới và hiển thị thông tin ví
@app.route('/create', methods=['POST'])
def create():
    account = web3.eth.account.create()
    address = account.address
    private_key = account._private_key.hex()
    balance = web3.eth.get_balance(address)

    return redirect(url_for('get_address', address=address))

# Trang thông tin ví: Hiển thị thông tin ví
@app.route('/address/<address>')
def get_address(address):
    balance = web3.eth.get_balance(address)
    return render_template('index.html', name='john', address=address, balance=balance)

# Trang gửi tiền: Hiển thị form để gửi tiền
@app.route('/send')
def send():
    return render_template('send.html')

# Trang nhận tiền: Hiển thị form để nhận tiền
@app.route('/receive')
def receive():
    return render_template('receive.html')

# Trang ký tài khoản: Hiển thị form để ký tài khoản
@app.route('/sign')
def sign():
    return render_template('sign.html')

# Trang thanh toán: Hiển thị form để thanh toán
@app.route('/pay')
def pay():
    return render_template('pay.html')

if __name__ == '__main__':
    app.run(debug=True)