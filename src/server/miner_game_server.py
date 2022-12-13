import os
import requests
import json

TON_API_URL = "https://tonapi.io"
TON_API_VERSION = "v1"
GET_COLLECTION_URL = "nft/getCollection"
GET_ACCOUNT_INFO_URL = "account/getInfo"
SEARCH_NFT_URL = "nft/searchItems"
SERVER_SIDE_KEY = os.getenv("SERVER_SIDE_KEY")

class MinerGameServer():
    def _request(self, action, params, extra_headers = None):
        url = "/".join([TON_API_URL, TON_API_VERSION, action])

        headers = {
            "Authorization": f"Bearer {SERVER_SIDE_KEY}"
        }
        if extra_headers:
            headers.update(extra_headers)

        response = requests.get(url, params=params, headers=headers)

        return response

    def get_gollection(self, collection_address):
        params = {
            "account": collection_address
        }
        return self._request(GET_COLLECTION_URL, params).text

    def get_account_info(self, account):
        params = {
            "account": account
        }
        return self._request(GET_ACCOUNT_INFO_URL, params).text
    
    def get_wallet_nft(self, wallet):
        params = {
            "owner": wallet,
            "limit": 1000,
            "offset": 0
        }
        return self._request(SEARCH_NFT_URL, params).text

    def preview_wallet_nft(self, wallet):
        params = {
            "owner": wallet,
            "limit": 1000,
            "offset": 0,
            "include_on_sale": True
        }
        response = self._request(SEARCH_NFT_URL, params)

        if response.status_code != 200:
            return "<p>There was an error during preview gen</p>"

        ntfs = json.loads(response.text)
        html = "<body>"
        html = f"{html}<h1>Not on sale</h1>"
        for nft in ntfs['nft_items']:
            if "sale" in nft:
                continue
            if "previews" in nft:
                preview = nft["previews"][1]["url"]
                html = f"{html}<img src='{preview}'/>"
        html = f"{html}<h1>On sale</h1>"
        for nft in ntfs['nft_items']:
            if "sale" not in nft:
                continue
            if "previews" in nft:
                preview = nft["previews"][1]["url"]
                price = float(nft["sale"]["price"]["value"]) / 1000000000.000
                html = f"{html}<h2>Хочу за это {price} тянок<h2><img src='{preview}'/>"
        html = f"{html}<body>"

        return html
