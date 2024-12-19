import requests
import os
import json
from datetime import datetime
from tzlocal import get_localzone
import warnings
import time
import argparse
import sys
from utils import *
from collections import Counter
from decimal import Decimal
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

    return {}


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
    saved_top_trader_addresses_file_path = f"{top_trader_addresses_dir}/{token_symbol}_{mint_address}.json"
    save_json_file(saved_top_trader_addresses_file_path, top_trader_addresses)

    return top_trader_addresses, token_symbol


def process_balance_updates_data(balance_updates_data,
                                 delta_time_seconds=180,
                                 consecutive_txns=5,
                                 amount_tolerance=5):

    bot_addresses = {}
    wallet_addresses_delta_transaction_time_dict = {}

    for balance_update in balance_updates_data:
        wallet_address = balance_update['BalanceUpdate']['Account']['Address']
        amount = balance_update['BalanceUpdate']['Amount']
        amount_in_usd = balance_update['BalanceUpdate']['AmountInUSD']
        check_amount = amount_in_usd or amount
        absolute_check_amount = Decimal(check_amount).copy_abs()
        time_str = balance_update['Block']['Time']
        time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')

        if wallet_address not in wallet_addresses_delta_transaction_time_dict:
            wallet_addresses_delta_transaction_time_dict[wallet_address] = []
        wallet_addresses_delta_transaction_time_dict[wallet_address].append({
            'time':
            time,
            'amount':
            absolute_check_amount
        })

    for wallet_address, data in wallet_addresses_delta_transaction_time_dict.items(
    ):
        sorted_data = sorted(data, key=lambda x: x['time'])
        consecutive_count = 1
        for i in range(1, len(sorted_data)):
            if ((sorted_data[i]['time'] -
                 sorted_data[i - 1]['time']).total_seconds()
                    <= delta_time_seconds) and (sorted_data[i]['amount']
                                                <= amount_tolerance):
                consecutive_count += 1
                if consecutive_count >= consecutive_txns:
                    bot_addresses[wallet_address] = True
                    break
            else:
                consecutive_count = 1

    return bot_addresses


def get_bot_addresses(mint_addresses,
                      max_no_of_wallets_per_batch=100,
                      count=8000):

    total_mint_addresses = len(mint_addresses)
    new_bot_addresses = {}

    for i in range(0, total_mint_addresses, max_no_of_wallets_per_batch):

        unique_wallets_batch = mint_addresses[i:i +
                                              max_no_of_wallets_per_batch]

        unique_wallets_batch_json = json.dumps(unique_wallets_batch)

        query = f"""
            query {{
            Solana {{
                BalanceUpdates(
                limit: {{count: {count}}}
                where: {{BalanceUpdate: {{Account: {{Address: {{in: {unique_wallets_batch_json}}}}}}}}}
                orderBy: {{descending: Block_Time}}
                ) {{
                Block {{
                    Time
                    Hash
                }}
                BalanceUpdate {{
                    Account {{
                    Address
                    }}
                    Amount
                    AmountInUSD
                }}
                }}
            }}
            }}
        """

        start_number = i + 1

        if i + max_no_of_wallets_per_batch > total_mint_addresses:
            end_number = total_mint_addresses
        else:
            end_number = i + max_no_of_wallets_per_batch

        print('Querying wallet addresses batch {} - {} out of {}'.format(
            start_number, end_number, total_mint_addresses))

        payload = {'query': query, 'variables': variables}
        data = bitqueryAPICall(payload)
        balance_updates_data = data.get('BalanceUpdates', [])
        bot_addresses = process_balance_updates_data(balance_updates_data)
        new_bot_addresses.update(bot_addresses)

    return new_bot_addresses


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
        '-a',
        '--address',
        type=str,
        default='',
        help=
        "Mint address to scan. If not provided, the script will scan all mint addresses from config.py."
    )
    parser.add_argument(
        '-d',
        '--directory',
        type=str,
        help=
        "The file directory that contains JSON files that contains the list of wallet addresses. REQURED for LOAD mode."
    )
    parser.add_argument(
        '-b',
        '--botcheck',
        type=str,
        default='Y',
        help=
        "Check for bot addresses. Y: Yes, N: No. Default is Y. Bot addresses will be saved in a JSON file."
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
    selected_mint_address = args.address
    mode = str(args.mode).upper()
    directory_path = args.directory
    bot_check = str(args.botcheck).upper()
    min_count = args.count

    if mode not in ['SCAN', 'LOAD']:
        print(
            "\nMode {} is not supported. Supported modes are SCAN and LOAD.\n".
            format(mode))
        sys.exit(1)

    if bot_check not in ['Y', 'N']:
        print(
            "\nBot check {} is not supported. Supported modes are Y and N.\n".
            format(bot_check))
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

    saved_data_base_dir = "./saved_data"
    top_trader_addresses_dir = saved_data_base_dir + f"/top_trader_addresses_{current_datetime}"
    bot_addresses_dir = saved_data_base_dir + "/bot_addresses"
    filtered_top_trader_addresses_dir = saved_data_base_dir + "/filtered_top_trader_addresses"

    flatten_top_trader_addresses = []
    graph_data = {'nodes': {}, 'edges': []}

    if mode == 'SCAN':
        os.makedirs(top_trader_addresses_dir, exist_ok=True)
        print("\nMode: {}".format(mode))
        if selected_mint_address:
            print("Mint Address selected: {}\n".format(selected_mint_address))

            print(
                'Retrieving top trader addresses for mint address: {}'.format(
                    selected_mint_address))
            top_trader_addresses, token_symbol = get_top_trader_addresses(
                selected_mint_address)

            flatten_top_trader_addresses.extend(top_trader_addresses)
            graph_data['nodes'][selected_mint_address] = {
                'mint_address': selected_mint_address,
                'symbol': token_symbol
            }

            for top_trader_address in top_trader_addresses:
                graph_data['edges'].append(selected_mint_address + '-' +
                                           top_trader_address)
        else:
            print("Mint Address selected: ALL")

            for mint_address in MINT_ADDRESSES:
                print('\nRetrieving top trader addresses for mint address: {}'.
                      format(mint_address))
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

    os.makedirs(bot_addresses_dir, exist_ok=True)
    loaded_bot_addresses = load_json_file(
        f"{bot_addresses_dir}/bot_addresses.json")
    excluded_addresses = {**EXCLUDED_ADDRESSES, **loaded_bot_addresses}
    wallet_counts = Counter(flatten_top_trader_addresses)
    wallet_counts = {
        key: value
        for key, value in wallet_counts.items()
        if key not in excluded_addresses
    }
    if bot_check == 'Y':
        new_bot_addresses = get_bot_addresses(list(wallet_counts.keys()))
        all_bot_addresses = {**loaded_bot_addresses, **new_bot_addresses}
        saved_bot_addresses_file_path = f"{bot_addresses_dir}/bot_addresses.json"
        if os.path.exists(saved_bot_addresses_file_path):
            os.remove(saved_bot_addresses_file_path)
        save_json_file(saved_bot_addresses_file_path, all_bot_addresses)
        excluded_addresses = {**excluded_addresses, **all_bot_addresses}

    repeated_wallets_dict = {
        wallet: count
        for wallet, count in wallet_counts.items() if count >= min_count
        and wallet != '' and wallet not in excluded_addresses
    }

    print('\nPrinting wallet addresses and their connection counts...')
    sorted_wallets = sorted(repeated_wallets_dict.items(),
                            key=lambda item: item[1],
                            reverse=True)
    for wallet, count in sorted_wallets:
        print(f'{wallet}: {count}')

    os.makedirs(filtered_top_trader_addresses_dir, exist_ok=True)
    filtered_top_trader_addresses_file_path = f"{filtered_top_trader_addresses_dir}/top_trader_addresses.json"
    if os.path.exists(filtered_top_trader_addresses_file_path):
        os.remove(filtered_top_trader_addresses_file_path)
    save_json_file(filtered_top_trader_addresses_file_path,
                   repeated_wallets_dict)

    plot_nodes_edges_graph(graph_data, repeated_wallets_dict,
                           excluded_addresses)

    print('\nTotal time taken: {:.2f} seconds'.format(time.time() -
                                                      start_time))
