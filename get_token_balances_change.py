import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import sys
import time
from utils import *
import dexscreener
from config import (VYBE_NETWORK_X_API_KEY, VYBE_NETWORK_QUERY_LIMIT,
                    MAX_RETRIES, RETRY_AFTER, EPSILON, MIN_MARKETCAP)

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
token_balances_update_dict = {}
mint_address_list = []

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
                    key = f'{name} ({symbol}) [{mint_address}]'
                    print('Add {} {} ({}) tokens'.format(amount, symbol, name))
                    if key not in token_balances_update_dict:
                        token_balances_update_dict[key] = amount
                        mint_address_list.append(mint_address)
                    else:
                        token_balances_update_dict[key] += amount
                else:
                    prev_amount = top_trader_token_balances_dict[
                        wallet_address][mint_address]['amount']
                    if amount > prev_amount + EPSILON:
                        delta = amount - prev_amount
                        key = f'{name} ({symbol}) [{mint_address}]'
                        print('Add {} {} ({}) tokens'.format(
                            delta, symbol, name))
                        if key not in token_balances_update_dict:
                            token_balances_update_dict[key] = delta
                            mint_address_list.append(mint_address)
                        else:
                            token_balances_update_dict[key] += delta
                    elif amount < prev_amount - EPSILON:
                        delta = amount - prev_amount
                        key = f'{name} ({symbol}) [{mint_address}]'
                        print('Subtract {} {} ({}) tokens'.format(
                            prev_amount - amount, symbol, name))
                        if key not in token_balances_update_dict:
                            token_balances_update_dict[key] = delta
                            mint_address_list.append(mint_address)
                        else:
                            token_balances_update_dict[key] += delta
                    top_trader_token_balances_dict[wallet_address][
                        mint_address]['amount'] = amount

            break_flag = True
            break

        else:
            retry_count += 1

            # print(
            #     'Query failed and return code is {}. Retrying ({}) after {} seconds...'
            #     .format(response.status_code, retry_count, RETRY_AFTER))

            time.sleep(RETRY_AFTER)

    if not break_flag:
        print('Maximum retries reached. Skipping...')

    count += 1

token_details_dict = dexscreener.get_token_details(mint_address_list)

print(
    f'\nSummarised token balances update (token marketcap >= {MIN_MARKETCAP}):'
)
for key, delta in token_balances_update_dict.items():
    key_splitted = key.split(' ')
    mint_address = key_splitted[-1][1:-1]
    token_details = token_details_dict.get(mint_address, {})
    market_cap = token_details.get('marketCap', 0)
    if market_cap >= MIN_MARKETCAP:
        print(f'{key}: {delta}')

if os.path.exists(top_trader_token_balances_file_path):
    os.remove(top_trader_token_balances_file_path)
save_json_file(top_trader_token_balances_file_path,
               top_trader_token_balances_dict)

print('\nTotal time taken: {:.2f} seconds'.format(time.time() - start_time))
