import requests
import json

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
    def get_full_rs(self, whale_id):
        json_data = {
            'index': whale_id,
        }
        response = requests.post('https://whales-club-bot-34uqt.ondigitalocean.app/api/bot/nft', headers=headers, json=json_data).text
        whale_json = json.loads(response)
        response = 'Whale not found'
        for nfts in whale_json['nfts']:
            if 'fullScore' in nfts:
                full_score = nfts['fullScore']
                response = 'The full score of the whale №' + str(whale_id) + ' is ' + str(full_score)
            else:
                response = 'Whale score is not defined'
        return response