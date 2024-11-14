from flask import *

def download_file(name, address, private_key):
    
    account_info = {
        "name": name,
        "address": address,
        "private_key": private_key
    }

    # Lưu thông tin vào một tệp JSON
    file_name = f"account_{name}.json"
    with open(file_name, "w") as file:
        json.dump(account_info, file, indent=4)

    # Trả về tệp JSON để tải xuống
    return send_file(file_name, as_attachment=True)