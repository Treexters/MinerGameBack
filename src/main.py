from flask import Flask, jsonify
from server.miner_game_server import MinerGameServer

app = Flask(__name__)

game_server = MinerGameServer()

@app.route('/check/<string:address>', methods=['GET'])
def get_collection(address):
    response = game_server.get_gollection(address)
    return response

@app.route('/account/<string:account>', methods=['GET'])
def get_account_info(account):
    response = game_server.get_account_info(account)
    return response

@app.route('/nft_by_wallet/<string:wallet>', methods=['GET'])
def get_wallet_nft(wallet):
    response = game_server.get_wallet_nft(wallet)
    return response

@app.route('/nft_by_wallet/<string:wallet>/preview', methods=['GET'])
def preview_wallet_nft(wallet):
    response = game_server.preview_wallet_nft(wallet)
    return response

if __name__ == '__main__':
    app.run(debug=True)