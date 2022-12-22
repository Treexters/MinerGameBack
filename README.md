# MinerGameBack
Right now no game is there, just experiments with ton api

# Setup DEV env in Windows
1. Install vs Code
2. Install python
3. Install pip
4. Add py and pip to PATH env variable
5. (Optional) Install https://visualstudio.microsoft.com/ru/visual-cpp-build-tools/
6. pip install -r requirements.txt

# How to run
1. Git clone this repo
2. Add `SERVER_SIDE_KEY` to environment variables
3. command shell to the src folder
4. `python main.py`
5. Now go to `http://127.0.0.1:5000` and proceed from there

# List of available endpoints for now
- `/check/<address>` - head-only info about collection with specified address
- `/account/<account>` - head-only info about account with specified address
- `/nft_by_wallet/<wallet>` - list of nft bound to an account (on sale ones are filtered)
- `/nft_by_wallet/<wallet>/preview` - image previews of nft bound to an account (with on sale ones)
- `/rs_by_whale/<whale>` - returns a full rarity score of a whale NFT
