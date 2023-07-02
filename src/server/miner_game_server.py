from abc import ABC, abstractmethod
import os
import time
import requests
import json
import statistics
import sqlite3
from sqlite3 import Connection, Cursor

TON_API_URL = "https://tonapi.io"
TON_API_VERSION = "v1"
GET_COLLECTION_URL = "nft/getCollection"
GET_ACCOUNT_INFO_URL = "account/getInfo"
SEARCH_NFT_URL = "nft/searchItems"
SERVER_SIDE_KEY = os.getenv("SERVER_SIDE_KEY")
DEFAULT_SCHEMA_ID = 2

TON_NANO_DIVIDER = 1000000000.000

class FieldSchema(ABC):
    pass

    def __init__(self, schema: str) -> None:
        self.schema = schema

    @abstractmethod
    def generate_field(self, dim_x, dim_y):
        pass

class DefaultSchema(FieldSchema):
    pass

    def generate_field(self, dim_x, dim_y):
        pass

class MinerGameServer():
    __db_connection: Connection
    cursor: Cursor

    def __init__(self) -> None:
        # sqlite3.threadsafety = 3
        self.__db_connection = sqlite3.connect("local.db", check_same_thread=False)
        self.cursor = self.__db_connection.cursor()
    
    def get_field(self, wallet):
        rows = self.cursor.execute(f"SELECT * from fields WHERE wid = '{wallet}' LIMIT 1")
        row = rows.fetchone()
        if not row:
            print("Creating new field")
            self.create_field(wallet, DEFAULT_SCHEMA_ID)

    def create_field(self, wallet, schema_id):
        schema_rows = self.cursor.execute(f"SELECT schema from fields_schemas where id = '{schema_id}' LIMIT 1")
        schema = schema_rows.fetchone()
        if not schema:
            print(f"No such schema with id {schema_id}")
            return
    
        schema_map: dict[int, FieldSchema] = {
            2: DefaultSchema
        }

        if schema_id not in schema_map:
            cls = DefaultSchema(schema[0])
        else: 
            cls = schema_map[schema_id](schema[0])

        field = cls.generate_field(5, 8)


    def _request(self, action, params, extra_headers = None):
        url = "/".join([TON_API_URL, TON_API_VERSION, action])

        headers = {
            "Authorization": f"Bearer {SERVER_SIDE_KEY}"
        }
        if extra_headers:
            headers.update(extra_headers)

        response = requests.get(url, params=params, headers=headers)

        return response

    def get_collection(self, collection_address):
        params = {
            "account": collection_address
        }
        return self._request(GET_COLLECTION_URL, params)

    def get_account_info(self, account):
        params = {
            "account": account
        }
        return self._request(GET_ACCOUNT_INFO_URL, params)
    
    def get_wallet_nft(self, wallet):
        params = {
            "owner": wallet,
            "limit": 1000,
            "offset": 0
        }
        return self._request(SEARCH_NFT_URL, params)
    
    def get_floor_by_collection(self, collection_address):
        collection = self.get_collection(collection_address).json()
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
            response = self._request(SEARCH_NFT_URL, params)
            nfts.extend(response.json()["nft_items"])
            # To not spam server
            time.sleep(1)
        
        # filter all nfts which is not on sale and have sale price (price == 0 means auction, which has no effect on floor price)
        on_sale = [nft for nft in nfts if "sale" in nft and int(nft["sale"]["price"]["value"]) > 0]
        floor_nft = min(on_sale, key=lambda x: int(x["sale"]["price"]["value"]))

        floor_price = float(floor_nft["sale"]["price"]["value"])/TON_NANO_DIVIDER
        floor_nft_name = floor_nft["metadata"]["name"]
        return f"{floor_price} ({floor_nft_name})"

    def get_average_collection_price(self, collection_address):
        collection = self.get_collection(collection_address).json()
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
            response = self._request(SEARCH_NFT_URL, params)
            nfts.extend(response.json()["nft_items"])
            # To not spam server
            time.sleep(1)

        on_sale = [nft for nft in nfts if "sale" in nft and int(nft["sale"]["price"]["value"]) > 0]
        on_sale.sort(key=lambda x: int(x["sale"]["price"]["value"]))
        count = len(on_sale)
        if count < 10:
            return "Less than 10 items on sale, it's better to check this collection manually"
        prices: list[float] = []
        for i in range(int(count/4)):
            del on_sale[0]
            del on_sale[len(on_sale)-1]
        for nft in on_sale:
            prices.extend([float(nft["sale"]["price"]["value"])])

        return f"Average: {str(statistics.fmean(prices)/TON_NANO_DIVIDER)}"


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
                price = float(nft["sale"]["price"]["value"]) / TON_NANO_DIVIDER
                html = f"{html}<h2>Хочу за это {price} тянок<h2><img src='{preview}'/>"
        html = f"{html}<body>"

        return html
