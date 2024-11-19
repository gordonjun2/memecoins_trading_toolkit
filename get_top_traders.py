import requests
import os
import json
from datetime import datetime
from tzlocal import get_localzone
import warnings
import time
import argparse
import sys
import shutil
from utils import *
from collections import Counter
from plot_top_traders_graph import plot_nodes_edges_graph
from config import (BITQUERY_CLIENT_ID, BITQUERY_CLIENT_SECRET,
                    BITQUERY_V1_API_KEY, BITQUERY_API_VERSION,
                    BITQUERY_API_VERSION_URL_MAP, variables, MAX_RETRIES,
                    RETRY_AFTER, MINT_ADDRESSES, EXCLUDED_ADDRESSES)

warnings.filterwarnings("ignore", module="urllib3")

### Functions ###


def generate_oAuth():

    url = "https://oauth2.bitquery.io/oauth2/token"

    payload = 'grant_type=client_credentials&client_id={}&client_secret={}&scope=api'.format(
        BITQUERY_CLIENT_ID, BITQUERY_CLIENT_SECRET)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=payload,
                                verify=False)
    resp = json.loads(response.text)

    print("========== oAuth's reponse ==========")
    print(resp)
    print('=====================================')

    access_token = resp['access_token']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    return headers


def get_api_base_url():

    if BITQUERY_API_VERSION not in BITQUERY_API_VERSION_URL_MAP:
        raise ValueError(
            f"API version {BITQUERY_API_VERSION} is not supported. Supported API versions are {list(BITQUERY_API_VERSION_URL_MAP.keys())}"
        )
    else:
        url = BITQUERY_API_VERSION_URL_MAP[BITQUERY_API_VERSION]

        return url


def bitqueryAPICall(payload, max_retries=MAX_RETRIES, retry_after=RETRY_AFTER):

    retry_count = 0

    while retry_count < max_retries:

        if BITQUERY_API_VERSION == 'v1':
            response = requests.post(url,
                                     json=payload,
                                     headers=headers,
                                     verify=False)
        else:
            response = requests.post(url,
                                     headers=headers,
                                     data=json.dumps(payload),
                                     verify=False)

        if response.status_code == 200:
            try:
                data = response.json().get('data', {}).get('Solana', {})

                if not isinstance(data, dict):
                    print(
                        'The retrieved data is in the wrong format. Skipping...'
                    )

                    data = []
            except:
                print('The data is missing. Skipping...')

                data = []

            if None in list(data.values()):
                retry_count += 1

                print(
                    'Query failed even though return code is 200. Retrying ({}) after {} seconds...'
                    .format(retry_count, retry_after))

                time.sleep(retry_after)

            else:
                return data

        elif response.status_code == 429:
            retry_count += 1

            print(
                'Query failed and return code is 429. API call limit might be reached. Retrying ({}) after {} seconds...'
                .format(retry_count, retry_after))

            time.sleep(retry_after)

        else:
            retry_count += 1

            print(
                'Query failed and return code is {}. Retrying ({})...'.format(
                    response.status_code, retry_count))

    print('Maximum retries reached. Skipping...')

    return []


def process_dex_trade_by_tokens_data(dex_trade_by_tokens_data):

    top_trader_addresses = []
    token_symbol = 'None'

    for top_trader in dex_trade_by_tokens_data:
        top_trader_address = top_trader['Trade']['Account']['Owner']
        token_symbol = top_trader['Trade']['Currency']['Symbol']

        top_trader_addresses.append(top_trader_address)

    return top_trader_addresses, token_symbol


def get_top_trader_addresses(mint_address, count=100):

    query = f"""
        query {{
        Solana(dataset: combined) {{
            DEXTradeByTokens(
            limit: {{count: {count}}}
            orderBy: {{descendingByField: "tokens"}}
            where: {{Trade: {{Currency: {{MintAddress: {{is: "{mint_address}"}}}}}}}}
            ) {{
            Trade {{
                Account {{
                Owner
                }}
                Currency {{
                Symbol
                }}
            }}
            tokens: sum(of: Trade_Amount)
            trades: count
            }}
        }}
        }}
    """

    payload = {'query': query, 'variables': variables}
    data = bitqueryAPICall(payload)
    dex_trade_by_tokens_data = data.get('DEXTradeByTokens', [])
    top_trader_addresses, token_symbol = process_dex_trade_by_tokens_data(
        dex_trade_by_tokens_data)
    saved_top_trader_addresses_file_path = f"{saved_data_folder_file_path}/top_trader_addresses_{token_symbol}_{mint_address}.json"
    save_json_file(saved_top_trader_addresses_file_path, top_trader_addresses)

    return top_trader_addresses, token_symbol


## Main Program ##

if __name__ == "__main__":

    # Get arguments from terminal
    parser = argparse.ArgumentParser(
        description="Get parameters for the script.")
    parser.add_argument('-m',
                        '--mode',
                        type=str,
                        default='SCAN',
                        help="SCAN: Save top trader wallet addresses, \
        LOAD: Skip the scan process and load the wallet addresses from a selected saved data folder"
                        )
    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help=
        "The file directory that contains JSON files that contains the list of wallet addresses. REQURED for LOAD mode."
    )
    parser.add_argument(
        '-c',
        '--count',
        type=int,
        default=3,
        help=
        "Minimum number of times each wallet address must appear to be displayed in the plot."
    )
    args = parser.parse_args()
    mode = str(args.mode).upper()
    directory_path = args.directory
    min_count = args.count

    if mode not in ['SCAN', 'LOAD']:
        print(
            "\nMode {} is not supported. Supported modes are SCAN and LOAD.\n".
            format(mode))
        sys.exit(1)

    # Start time for the script
    start_time = time.time()

    # Get datetime
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_timezone = get_localzone()

    url = get_api_base_url()

    if BITQUERY_API_VERSION == 'v1':
        headers = {'X-API-KEY': BITQUERY_V1_API_KEY}
    else:
        headers = generate_oAuth()

    flatten_top_trader_addresses = []
    graph_data = {'nodes': {}, 'edges': []}

    if mode == 'SCAN':

        print("\nMode: {}".format(mode))

        saved_data_folder_file_path = f"./saved_data_{current_datetime}"
        if os.path.exists(saved_data_folder_file_path):
            shutil.rmtree(saved_data_folder_file_path)
            print('\nDeleted existing directory: {}'.format(
                saved_data_folder_file_path))

        os.makedirs(saved_data_folder_file_path)

        for mint_address in MINT_ADDRESSES:
            print(
                'Retrieving top trader addresses for mint address: {}'.format(
                    mint_address))
            top_trader_addresses, token_symbol = get_top_trader_addresses(
                mint_address)

            flatten_top_trader_addresses.extend(top_trader_addresses)
            graph_data['nodes'][mint_address] = {
                'mint_address': mint_address,
                'symbol': token_symbol
            }

            for top_trader_address in top_trader_addresses:
                graph_data['edges'].append(mint_address + '-' +
                                           top_trader_address)

    else:

        print("\nMode: {}".format(mode))
        print("Directory Path to the List of Wallet Addresses: {}".format(
            directory_path))

        if directory_path in ['', None]:
            print(
                "\nPlease provide the directory path to load the list of wallet addresses in INPUT mode.\n"
            )
            sys.exit(1)

        try:
            for file_name in os.listdir(directory_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(directory_path, file_name)
                    with open(file_path, 'r') as f:
                        top_trader_addresses = json.load(f)

                    file_name = file_name.replace('.json', '')
                    file_name_split = file_name.split('_')
                    mint_address = file_name_split[-1]
                    token_symbol = file_name_split[-2]

                    flatten_top_trader_addresses.extend(top_trader_addresses)
                    graph_data['nodes'][mint_address] = {
                        'mint_address': mint_address,
                        'symbol': token_symbol
                    }

                    for top_trader_address in top_trader_addresses:
                        graph_data['edges'].append(mint_address + '-' +
                                                   top_trader_address)

        except FileNotFoundError:
            print("\nThe directory was not found or is invalid.\n")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"\nError decoding JSON in file: {file_path}. Error: {e}\n")
            sys.exit(1)

    print('\nGraph data generated...')

    wallet_counts = Counter(flatten_top_trader_addresses)
    repeated_wallets_dict = {
        wallet: count
        for wallet, count in wallet_counts.items() if count >= min_count
        and wallet != '' and wallet not in EXCLUDED_ADDRESSES
    }

    print('\nPrinting wallet addresses and their connection counts...')
    sorted_wallets = sorted(repeated_wallets_dict.items(),
                            key=lambda item: item[1],
                            reverse=True)
    for wallet, count in sorted_wallets:
        print(f'{wallet}: {count}')

    plot_nodes_edges_graph(graph_data, repeated_wallets_dict)

    print('\nTotal time taken: {:.2f} seconds'.format(time.time() -
                                                      start_time))
