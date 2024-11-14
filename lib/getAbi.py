import json

def getAbi():
    with open('abi/abi.json') as f:
        abi = json.load(f)
    return abi

