import requests
import json
import time
import html
import datetime
from prettytable import PrettyTable
from src.server.miner_game_server import MinerGameServer
from src.server.miner_game_server import TON_NANO_DIVIDER

SEARCH_NFT_URL = "nft/searchItems"
game_server = MinerGameServer()

headers = {
    'authority': 'whales-club-bot-34uqt.ondigitalocean.app',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://tonwhales.com',
    'referer': 'https://tonwhales.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-api-key': 'M5eFoUFDJq',
}

class WhalesReqs():
    def get_full_rs(self, whale_number):
        #print("Looking for the whale #" + str(whale_number) + " score")
        json_data = {
            "index": whale_number,
        }
        response = requests.post("https://whales-club-bot-34uqt.ondigitalocean.app/api/bot/nft", headers=headers, json=json_data).text
        whale_json = json.loads(response)
        response = "Whale №" + str(whale_number) + " not found"
        for nfts in whale_json["nfts"]:
            if "fullScore" in nfts:
                full_score = int(nfts["fullScore"])
                address = str(nfts["address"])
                response = "The full score of the whale №" + str(whale_number) + " is " + str(full_score)
            else:
                response = "Whale №" + str(whale_number) + " score is not defined"
        print(response)
        return full_score, address

    def top_whales_on_sale(self):
        collection_address = "EQDvRFMYLdxmvY3Tk-cfWMLqDnXF_EclO2Fp4wwj33WhlNFT"
        collection = game_server.get_collection(collection_address).json()
        total_items = int(collection["next_item_index"])

        if total_items == -1:
            # Out of scope due to
            #  https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#get-methods-1
            # -1 value of next_item_index is used to indicate non-sequential collections, such collections
            # should provide their own way for index generation / item enumeration
            return "Not supported NFT collection enumeration"

        limit = 1000
        nfts: list[dict] = []
        for offset in range(0, total_items, limit):
            params = {
                "collection": collection_address,
                "limit": limit,
                "offset": offset,
            }
            response = game_server._request(SEARCH_NFT_URL, params)
            nfts.extend(response.json()["nft_items"])
            # To not spam server
            time.sleep(1)

        on_sale = [nft for nft in nfts if "sale" in nft and int(nft["sale"]["price"]["value"]) > 0]

        whales_table = PrettyTable(["Whale", "Price", "Rarity", "Price/Rarity"])
        whales_list = [[], []]

        for nft in on_sale:
            wh_name = nft["metadata"]["name"]
            wh_number = wh_name[wh_name.rfind("#")+1:]
            wh_img_name = f"<img src='https://whales.infura-ipfs.io/ipfs/QmQ5QiuLBEmDdQmdWcEEh2rsW53KWahc63xmPVBUSp4teG/{wh_number}.png' style='max-width: 100%; max-height: 100%; width: 100px;'/>"
            wh_img_name = f"<p style='margin-bottom: 10px;'>{wh_img_name}</br>"
            wh_price = float(nft["sale"]["price"]["value"])/TON_NANO_DIVIDER
            wh_rarity, wh_address = self.get_full_rs(wh_number)
            wh_index = round(wh_price/wh_rarity, 3)
            wh_img_name = f"{wh_img_name}<a href='https://getgems.io/collection/{collection_address}/{wh_address}' target='_blank'>{wh_name}</a></p>"
            wh_rarity = f"<a href='https://tonwhales.com/club/preview/{wh_number}' target='_blank'>{wh_rarity}</a>"
            whales_table.add_row([wh_img_name, wh_price, wh_rarity, wh_index])

        top_whales_1 = whales_table.get_html_string(start=0, end=10, sortby="Price/Rarity", format=True, attributes={"align":"center"})
        top_whales_1 = html.unescape(top_whales_1)
        top_whales_2 = whales_table.get_html_string(start=10, end=20, sortby="Price/Rarity", format=True, attributes={"align":"center"})
        top_whales_2 = html.unescape(top_whales_2)
        top_whales_3 = whales_table.get_html_string(start=20, end=30, sortby="Price/Rarity", format=True, attributes={"align":"center"})
        top_whales_3 = html.unescape(top_whales_3)

        page_made_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        wh_html_page = "<style>body {text-align: center; background-color: #0c2340; color: white;} h {font-size: 40px; font-weight: bold; color: #00bfff;}" \
                       "a {color: #00bfff; text-decoration: none;}" \
                       "table {border-collapse: collapse; width: 100%; max-width: 800px; margin: 0 auto; background-color: #1a5276; box-shadow: 0px 0px 10px #00bfff;}" \
                       "th, td {padding: 10px; text-align: center; border: 1px solid white;} th {background-color: #0c2340; color: #00bfff; font-weight: bold;}" \
                       "tr:nth-child(even) {background-color: #154360;}" \
                       "img {max-width: 100%; max-height: 100%; width: 100px;} p {font-size: 20px; margin-bottom: 10px;}" \
                       "div:nth-child(1), div:nth-child(2), div:nth-child(3) {float: left; width: calc(100%/3); min-width: 400px; padding: 10px; box-sizing: border-box;}</style>" \
                       f"<body><h>Top 30 whales NFT on sale by price/rarity</h>" \
                       f"</br><p>Find more about the Whales Club here: <a href='https://tonwhales.com/club' target='_blank'>tonwhales.com/club</a></p>" \
                       f"<p>The page was generated at {page_made_date} (GMT+3)</p><div style='margin: 0 auto; width: 70%; min-width: 400px;'><div>" \
                       f"<p style='margin: 0 auto; font-size: 30; font-weight: bold'>1-10</p>{top_whales_1}</div>" \
                       f"<div><p style='margin: 0 auto; font-size: 30; font-weight: bold'>11-20</p>{top_whales_2}</div><div>" \
                       f"<p style='margin: 0 auto; font-size: 30; font-weight: bold'>21-30</p>{top_whales_3}</div></div></body>"

        return wh_html_page
