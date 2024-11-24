import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import sys
import time
from utils import *
from config import VYBE_NETWORK_X_API_KEY, VYBE_NETWORK_QUERY_LIMIT, MAX_RETRIES, RETRY_AFTER

urllib3.disable_warnings(InsecureRequestWarning)

start_time = time.time()

saved_data_base_dir = "./saved_data"
filtered_top_trader_addresses_dir = saved_data_base_dir + "/filtered_top_trader_addresses"
loaded_top_trader_addresses = load_json_file(
    f"{filtered_top_trader_addresses_dir}/top_trader_addresses.json")
top_trader_token_balances_dir = saved_data_base_dir + "/top_trader_token_balances"
os.makedirs(top_trader_token_balances_dir, exist_ok=True)
top_trader_token_balances_file_path = f"{top_trader_token_balances_dir}/top_trader_token_balances.json"

if not loaded_top_trader_addresses:
    print("No top trader addresses found. Exiting...")
    sys.exit(1)
else:
    top_trader_token_balances_dict = load_json_file(
        top_trader_token_balances_file_path)

count = 1
total_top_trader_addresses = len(loaded_top_trader_addresses)

for wallet_address in loaded_top_trader_addresses:

    retry_count = 0
    break_flag = False
    print('\n')

    while retry_count < MAX_RETRIES:

        url = "https://api.vybenetwork.xyz/account/token-balance/{}?includeNoPriceBalance=true&limit={}&page=0".format(
            wallet_address, VYBE_NETWORK_QUERY_LIMIT)

        headers = {
            "accept": "application/json",
            "X-API-KEY": VYBE_NETWORK_X_API_KEY
        }

        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            tokens_data = response.json().get('data', [])
            print('No. of tokens queried from wallet address {} ({}/{}): {}'.
                  format(wallet_address, count, total_top_trader_addresses,
                         len(tokens_data)))

            if wallet_address not in top_trader_token_balances_dict:
                top_trader_token_balances_dict[wallet_address] = {}

            for token_data in tokens_data:
                symbol = token_data.get('symbol', '')
                name = token_data.get('name', '')
                mint_address = token_data.get('mintAddress', '')
                amount = token_data.get('amount', 0)
                if isinstance(amount, str):
                    amount = float(amount)
                if mint_address not in top_trader_token_balances_dict[
                        wallet_address]:
                    top_trader_token_balances_dict[wallet_address][
                        mint_address] = {
                            'symbol': symbol,
                            'name': name,
                            'amount': amount,
                        }
                    print('Bought {} {} ({}) tokens'.format(
                        amount, symbol, name))
                else:
                    prev_amount = top_trader_token_balances_dict[
                        wallet_address][mint_address]['amount']
                    if amount > prev_amount:
                        print('Bought {} {} ({}) tokens'.format(
                            amount - prev_amount, symbol, name))
                    elif amount < prev_amount:
                        print('Sold {} {} ({}) tokens'.format(
                            prev_amount - amount, symbol, name))
                    top_trader_token_balances_dict[wallet_address][
                        mint_address]['amount'] = amount

            break_flag = True
            break

        else:
            retry_count += 1

            print(
                'Query failed and return code is {}. Retrying ({}) after {} seconds...'
                .format(response.status_code, retry_count, RETRY_AFTER))

            time.sleep(RETRY_AFTER)

    if not break_flag:
        print('Maximum retries reached. Skipping...')

    count += 1

if os.path.exists(top_trader_token_balances_file_path):
    os.remove(top_trader_token_balances_file_path)
save_json_file(top_trader_token_balances_file_path,
               top_trader_token_balances_dict)

print('\nTotal time taken: {:.2f} seconds'.format(time.time() - start_time))
