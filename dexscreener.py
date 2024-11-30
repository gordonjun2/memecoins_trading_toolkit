import requests
import time
import warnings
from config import (MAX_RETRIES, RETRY_AFTER)

warnings.filterwarnings("ignore", module="urllib3")


def get_token_details(mint_addresses,
                      max_retries=MAX_RETRIES,
                      retry_after=RETRY_AFTER):

    token_details_dict = {}
    total_mint_addresses = len(mint_addresses)
    count = 1

    print('\n')

    for i in range(0, total_mint_addresses):

        print('Querying token details {} out of {}'.format(
            i + 1, total_mint_addresses))

        mint_address = mint_addresses[i]

        url = "https://api.dexscreener.com/latest/dex/tokens/{}".format(
            mint_address)

        headers = {
            "accept": "application/json",
        }

        retry_count = 0

        while retry_count < max_retries:

            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:

                token_details = response.json().get('pairs', [])

                if not token_details:

                    print(
                        'Token details for mint address {} cannot be found. Skipping...'
                        .format(mint_address))

                else:

                    for token in token_details:
                        count += 1
                        mint_address = token.get('baseToken',
                                                 {}).get('address', '')

                        if not mint_address:
                            continue

                        if mint_address not in token_details_dict:
                            token_details_dict[mint_address] = {
                                'chainId':
                                token.get('chainId', ''),
                                'dexId':
                                token.get('dexId', ''),
                                'name':
                                token.get('baseToken', {}).get('name', ''),
                                'symbol':
                                token.get('baseToken', {}).get('symbol', ''),
                                'volume':
                                token.get('volume', {}),
                                'priceChange':
                                token.get('priceChange', {}),
                                'liquidity':
                                token.get('liquidity', {}),
                                'fdv':
                                token.get('fdv', 0),
                                'info':
                                token.get('info', {}),
                                'marketCap':
                                token.get('marketCap', 0),
                            }

                break

            else:
                retry_count += 1

                print(
                    'Query failed and return code is {}. Retrying ({}) after {} seconds...'
                    .format(response.status_code, retry_count, retry_after))

                time.sleep(retry_after)

        if retry_count >= max_retries:
            print('Maximum retries reached. Skipping the rest...')
            break

    return token_details_dict
