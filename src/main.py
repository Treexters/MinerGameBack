from flask import Flask, jsonify
from server.miner_game_server import MinerGameServer
from whales.whales_requests import WhalesReqs

app = Flask(__name__)

game_server = MinerGameServer()

@app.route('/check/<string:address>', methods=['GET'])
def get_collection(address):
    response = game_server.get_collection(address)
    return response.text

@app.route('/account/<string:account>', methods=['GET'])
def get_account_info(account):
    response = game_server.get_account_info(account)
    return response.text

@app.route('/nft_by_wallet/<string:wallet>', methods=['GET'])
def get_wallet_nft(wallet):
    response = game_server.get_wallet_nft(wallet)
    return response.text

@app.route('/nft_by_wallet/<string:wallet>/preview', methods=['GET'])
def preview_wallet_nft(wallet):
    response = game_server.preview_wallet_nft(wallet)
    return response

@app.route('/floor_by_collection/<string:collection>', methods=['GET'])
def get_floor_by_collection(collection):
    response = game_server.get_floor_by_collection(collection)
    return response

@app.route('/average_collection_price/<string:collection>', methods=['GET'])
def get_average_collection_price(collection):
    response = game_server.get_average_collection_price(collection)
    return response

whales_reqs = WhalesReqs()

@app.route('/rs_by_whale/<string:whale>', methods=['GET'])
def get_full_rs(whale):
    wh_score, wh_address = whales_reqs.get_full_rs(whale)
    response = f"The full score of the whale #{whale} is {wh_score}"
    return response

@app.route('/top_whales_on_sale/', methods=['GET'])
def top_whales_on_sale():
    response = whales_reqs.top_whales_on_sale()
    return response

if __name__ == '__main__':
    app.run(debug=True)