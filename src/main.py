from flask import Flask, jsonify, request
from server.miner_game_server import MinerGameServer
from whales.whales_requests import WhalesReqs
from flask_socketio import SocketIO, join_room
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
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

@app.route('/ton_connect_shenanigans/', methods=['GET'])
def ton_connect_shenanigans():
    response = """<script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js"></script>
    <script>
        const connector = new TonConnectSDK.TonConnect({ manifestUrl: 'http://127.0.0.1:5000/ton_connect_json' });

        connector.restoreConnection();
        const walletsList = connector.getWallets();

        walletsList.then(function(result) {
            str = JSON.stringify(result, null, 4);
            alert(str)
        });
        
    </script>
    """
    return response

@app.route('/ton_connect_json/', methods=['GET'])
def ton_connect_json():
    response = """
    {
    "url": "http://127.0.0.1:5000/",
    "name": "MinerGame",
    "iconUrl": "https://img.icons8.com/wired/512/share-2.png"
    }
    """
    return response

@socketio.on('connect')
def test_connect():
    # TODO: Remove on production stage. 
    # Send sid to client for debug purposes
    socketio.send(request.sid, to=request.sid)

@socketio.on('auth')
def auth(data):
    wallet = data["wallet"]
    token = data["token"]

    # TODO: TON Connect 2.0 check token or whatever it gives
    pass

    # Put client to a room with wallet as key
    join_room(wallet)

    # TODO: Remove on production stage
    # Send debug output to exactly this wallet clients
    socketio.emit("auth_successfull", f"Auth with wallet {wallet} was successfull", to=wallet)

@socketio.on('get_field')
def auth(data):
    wallet = data["wallet"]
    token = data["token"]

    # TODO: Check wallet and token

    game_server.get_field(wallet)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)