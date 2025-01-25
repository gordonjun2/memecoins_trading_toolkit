import requests
import os
import time
import logging
from utils import *
import dexscreener
import telebot
import re
import argparse
from pytrends.request import TrendReq
import pandas as pd
import random
from config import (VYBE_NETWORK_X_API_KEYS, VYBE_NETWORK_QUERY_LIMIT,
                    MAX_RETRIES, RETRY_AFTER, EPSILON, MIN_MARKETCAP,
                    WALLET_ADDRESSES_TO_INCLUDE_DICT, TELEGRAM_BOT_TOKEN, USER_ID,
                    TEST_TG_CHAT_ID, MIN_BUY_AMOUNT_USD, MIN_SELL_AMOUNT_USD, 
                    RECENT_N_DAYS_INTEREST)

logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


def get_token_balance_change(mode, 
                             chat_id,
                             logger=logger,
                             get_token_details=True,
                             send_to_tg=True):

    X_API_KEYS = VYBE_NETWORK_X_API_KEYS or os.getenv(
        'VYBE_NETWORK_X_API_KEYS')
    random.shuffle(X_API_KEYS)

    start_time = time.time()

    saved_data_base_dir = "./saved_data"

    filtered_top_trader_addresses_dir = saved_data_base_dir + "/filtered_top_trader_addresses"

    loaded_top_trader_addresses = load_json_file(
        f"{filtered_top_trader_addresses_dir}/top_trader_addresses.json")
    loaded_top_trader_addresses = list(loaded_top_trader_addresses.keys())
    wallet_addresses_to_include = list(WALLET_ADDRESSES_TO_INCLUDE_DICT.keys())
    loaded_top_trader_addresses.extend(wallet_addresses_to_include)
    loaded_top_trader_addresses = set(loaded_top_trader_addresses)

    top_trader_token_balances_dir = saved_data_base_dir + "/top_trader_token_balances"
    os.makedirs(top_trader_token_balances_dir, exist_ok=True)
    top_trader_token_balances_file_path = f"{top_trader_token_balances_dir}/top_trader_token_balances.json"

    seen_token_addresses_dir = saved_data_base_dir + "/seen_token_addresses"
    os.makedirs(seen_token_addresses_dir, exist_ok=True)
    seen_token_addresses_file_path = f"{seen_token_addresses_dir}/seen_token_addresses.json"

    seen_token_addresses_new_mode_dir = saved_data_base_dir + "/seen_token_addresses_new_mode"
    os.makedirs(seen_token_addresses_new_mode_dir, exist_ok=True)
    seen_token_addresses_new_mode_file_path = f"{seen_token_addresses_new_mode_dir}/seen_token_addresses_new_mode.json"

    if not loaded_top_trader_addresses:
        logger.error("No top trader addresses found. Exiting...")
        return ''

    top_trader_token_balances_dict = load_json_file(
        top_trader_token_balances_file_path)
    seen_token_addresses_dict = load_json_file(
        seen_token_addresses_file_path)
    seen_token_addresses_new_mode_dict = load_json_file(
        seen_token_addresses_new_mode_file_path)

    count = 1
    total_top_trader_addresses = len(loaded_top_trader_addresses)
    token_balances_update_dict = {}
    mint_address_list = []
    loop_count = 0

    for wallet_address in loaded_top_trader_addresses:

        retry_count = 0
        break_flag = False
        print('\n')

        while retry_count < MAX_RETRIES:

            url = "https://api.vybenetwork.xyz/account/token-balance/{}?includeNoPriceBalance=true&limit={}&page=0".format(
                wallet_address, VYBE_NETWORK_QUERY_LIMIT)

            key_index = loop_count % len(X_API_KEYS)
            api_key = X_API_KEYS[key_index]
            headers = {"accept": "application/json", "X-API-KEY": api_key}

            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                tokens_data = response.json().get('data', [])
                print(
                    'No. of tokens queried from wallet address {} ({}/{}): {}'.
                    format(wallet_address, count, total_top_trader_addresses,
                           len(tokens_data)))

                if wallet_address not in top_trader_token_balances_dict:
                    top_trader_token_balances_dict[wallet_address] = {}

                for token_data in tokens_data:
                    symbol = token_data.get('symbol', '')
                    name = token_data.get('name', '')
                    mint_address = token_data.get('mintAddress', '')
                    key = f'{name} ({symbol}) [{mint_address}]'
                    amount = token_data.get('amount', 0)
                    price_usd = token_data.get('priceUsd', 0)

                    if isinstance(amount, str):
                        amount = float(amount)
                    if price_usd:
                        if isinstance(price_usd, str):
                            price_usd = float(price_usd)
                    else:
                        price_usd = 0
                    amount_usd = round(amount * price_usd, 2)
                    
                    if mint_address not in top_trader_token_balances_dict[
                            wallet_address]:
                        top_trader_token_balances_dict[wallet_address][
                            mint_address] = {
                                'symbol': symbol,
                                'name': name,
                                'amount': amount,
                            }
                        print('Add {} {} ({}) tokens'.format(
                            amount, symbol, name))
                        if key not in token_balances_update_dict:
                            token_balances_update_dict[key] = {}
                            token_balances_update_dict[key]['amount'] = amount
                            token_balances_update_dict[key]['amount_usd'] = amount_usd
                            token_balances_update_dict[key]['count'] = 1
                            token_balances_update_dict[key]['wallet_addresses'] = { wallet_address: amount_usd }
                            mint_address_list.append(mint_address)
                        else:
                            token_balances_update_dict[key]['amount'] += amount
                            token_balances_update_dict[key]['amount_usd'] += amount_usd
                            token_balances_update_dict[key]['count'] += 1
                            token_balances_update_dict[key]['wallet_addresses'][wallet_address] = amount_usd
                    else:
                        prev_amount = top_trader_token_balances_dict[
                            wallet_address][mint_address]['amount']
                        if amount > prev_amount + EPSILON:
                            delta = amount - prev_amount
                            print('Add {} {} ({}) tokens'.format(
                                delta, symbol, name))
                            delta_usd = round(delta * price_usd, 2)
                            if key not in token_balances_update_dict:
                                token_balances_update_dict[key] = {}
                                token_balances_update_dict[key][
                                    'amount'] = delta
                                token_balances_update_dict[key]['amount_usd'] = delta_usd
                                token_balances_update_dict[key]['count'] = 1
                                token_balances_update_dict[key]['wallet_addresses'] = { wallet_address: delta_usd }
                                mint_address_list.append(mint_address)
                            else:
                                token_balances_update_dict[key][
                                    'amount'] += delta
                                token_balances_update_dict[key]['amount_usd'] += delta_usd
                                token_balances_update_dict[key]['count'] += 1
                                token_balances_update_dict[key]['wallet_addresses'][wallet_address] = delta_usd
                        elif amount < prev_amount - EPSILON:
                            delta = amount - prev_amount
                            print('Subtract {} {} ({}) tokens'.format(
                                prev_amount - amount, symbol, name))
                            delta_usd = round(delta * price_usd, 2)
                            if key not in token_balances_update_dict:
                                token_balances_update_dict[key] = {}
                                token_balances_update_dict[key][
                                    'amount'] = delta
                                token_balances_update_dict[key]['amount_usd'] = delta_usd
                                token_balances_update_dict[key]['count'] = 1
                                token_balances_update_dict[key]['wallet_addresses'] = { wallet_address: delta_usd }
                                mint_address_list.append(mint_address)
                            else:
                                token_balances_update_dict[key][
                                    'amount'] += delta
                                token_balances_update_dict[key]['amount_usd'] += delta_usd
                                token_balances_update_dict[key]['count'] += 1
                                token_balances_update_dict[key]['wallet_addresses'][wallet_address] = delta_usd
                        top_trader_token_balances_dict[wallet_address][
                            mint_address]['amount'] = amount

                    if mint_address not in seen_token_addresses_dict:
                        if key in token_balances_update_dict:
                            token_balances_update_dict[key]['is_new'] = True
                        seen_token_addresses_dict[mint_address] = True

                loop_count += 1
                break_flag = True
                break

            else:
                retry_count += 1

                # print(
                #     'Query failed and return code is {}. Retrying ({}) after {} seconds...'
                #     .format(response.status_code, retry_count, RETRY_AFTER))

                loop_count += 1
                time.sleep(RETRY_AFTER)

        if not break_flag:
            logger.error('Maximum retries reached. Skipping...')

        count += 1

    if os.path.exists(top_trader_token_balances_file_path):
        os.remove(top_trader_token_balances_file_path)
    save_json_file(top_trader_token_balances_file_path,
                   top_trader_token_balances_dict)

    if os.path.exists(seen_token_addresses_file_path):
        os.remove(seen_token_addresses_file_path)
    save_json_file(seen_token_addresses_file_path,
                   seen_token_addresses_dict)

    if get_token_details:
        token_details_dict = dexscreener.get_token_details(mint_address_list)
        tg_msg_list = []

        terminal_msg = f'\nSummarised token balances update (token marketcap >= {MIN_MARKETCAP:,}):'
        print(terminal_msg)
        terminal_output = terminal_msg
        tg_msg_title_list = [
            f'**Summarised token balances update (token marketcap >= {MIN_MARKETCAP:,}):**\n'
        ]

        sorted_data = [{
            'key': key,
            **value
        } for key, value in sorted(
            token_balances_update_dict.items(),
            key=lambda x: (
                not x[1].get('is_new', False),
                -x[1].get('amount_usd', 0),
                -x[1]['count']
            )
        )]

        pytrends = TrendReq(hl='en-US', tz=360)

        for data in sorted_data:
            key = data['key']
            key_splitted = key.split(' ')
            mint_address = key_splitted[-1][1:-1]
            token_details = token_details_dict.get(mint_address, {})
            market_cap = token_details.get('marketCap', 0)
            if market_cap >= MIN_MARKETCAP:
                delta = data['amount']
                count = data['count']
                delta_usd = data['amount_usd']

                if (delta_usd >= 0) and (delta_usd <= MIN_BUY_AMOUNT_USD):
                    continue
                elif (delta_usd < 0) and (abs(delta_usd) <= MIN_SELL_AMOUNT_USD):
                    continue

                if mode == 'NEW' and mint_address in seen_token_addresses_new_mode_dict:
                    continue

                delta_usd_str = "{:,.2f}".format(delta_usd)
                is_new = data.get('is_new')

                key += ' '
                if is_new:
                    key += '🆕'
                if delta > 0:
                    key += '🟢'
                else:
                    key += '🔴'

                token_dexscreener = f'https://dexscreener.com/solana/{mint_address}'
                token_telegram = ''
                token_twitter = ''
                token_socials_detail = token_details.get('info', {}).get(
                    'socials', [])
                for token_social in token_socials_detail:
                    if token_social['type'] == 'telegram':
                        token_telegram = token_social.get('url', '')
                    elif token_social['type'] == 'twitter':
                        token_twitter = token_social.get('url', '')

                try:
                    token_symbol = key_splitted[1][1:-1]
                    pytrends.build_payload([token_symbol], cat=0, timeframe='today 1-m', geo='', gprop='')
                    interest_over_time_df = pytrends.interest_over_time()
                    interest_over_time_df.index = pd.to_datetime(interest_over_time_df.index)
                    interest_over_time_df.index = interest_over_time_df.index.tz_localize('UTC').tz_convert('Asia/Singapore')
                    recent_interest = interest_over_time_df.tail(RECENT_N_DAYS_INTEREST)
                    recent_interest = recent_interest.astype(str)
                    token_symbol_recent_interest_list = recent_interest[token_symbol].tolist()
                    token_symbol_recent_interest_str = ', '.join(token_symbol_recent_interest_list)
                except:
                    token_symbol_recent_interest_str = 'Data unavailable'

                terminal_msg = f'{key}:\nNo. of smart wallets interacted: {count}\nNet amount added: {delta}\nNet amount added (in USD): ${delta_usd_str}\nMarket cap: {market_cap}\nDEX Screener: {token_dexscreener}\nTwitter: {token_twitter}\nTelegram: {token_telegram}\n\nSmart wallets that interacted:\n'
                escaped_key = re.escape(key)
                escaped_key = escaped_key.replace(r'\ ', ' ')
                tg_msg = (
                        f"*_**{escaped_key}**_*\n"
                        f"No. of smart wallets interacted: {count}\n"
                        f"Net amount added: {delta}\n"
                        f"Net amount added (in USD): ${delta_usd_str}\n"
                        f"Market cap: {market_cap:,}\n"
                        f"[DEX Screener]({token_dexscreener}) | [Twitter]({token_twitter}) | [Telegram]({token_telegram})\n"
                        f"\n"
                        f"Smart wallets that interacted:\n"
                    )

                wallet_addresses = data.get('wallet_addresses')

                for wallet_address, delta_usd in wallet_addresses.items():
                    wallet_label = WALLET_ADDRESSES_TO_INCLUDE_DICT.get(wallet_address, wallet_address[:4] + '...' + wallet_address[-4:])
                    delta_usd_str = "{:,.2f}".format(abs(delta_usd))
                    if delta_usd > 0:
                        msg = f"- {wallet_label} bought ${delta_usd_str} worth.\n"
                    else:
                        msg = f"- {wallet_label} sold ${delta_usd_str} worth.\n"
                    terminal_msg += msg
                    tg_msg += msg

                msg = f"\nGoogle Trends' interest score of the token symbol over the past {RECENT_N_DAYS_INTEREST} days:\n"
                msg += f"{token_symbol_recent_interest_str}\n"

                terminal_msg += msg
                tg_msg += msg

                print(terminal_msg)
                terminal_output += '\n' + terminal_msg
                tg_msg += '\n---\n'
                tg_msg_list.append(tg_msg)

                if mint_address not in seen_token_addresses_new_mode_dict:
                    seen_token_addresses_new_mode_dict[mint_address] = True

        if os.path.exists(seen_token_addresses_new_mode_file_path):
            os.remove(seen_token_addresses_new_mode_file_path)
        save_json_file(seen_token_addresses_new_mode_file_path,
                    seen_token_addresses_new_mode_dict)

        file_path = "latest_token_balances_change_terminal_output.txt"
        with open(file_path, "w") as file:
            file.write(terminal_output)

        print(f"\nTerminal output saved to {file_path}\n")

        if send_to_tg:
            if tg_msg_list:
                print("Sending token balances updates to Telegram...\n")
                bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN, threaded=False)
                tg_msg_title_list.extend(tg_msg_list)
                chunks = chunk_message(tg_msg_title_list)
                for chunk in chunks:
                    retry_count = 0
                    while retry_count < MAX_RETRIES:
                        try:
                            bot.send_message(chat_id,
                                             chunk,
                                             parse_mode='MarkdownV2')
                            time.sleep(3)
                            break
                        except:
                            retry_count += 1
                            time.sleep(60)
                    else:
                        print(
                            "Max retries reached. No new message will be sent.\n"
                        )
                        break

                print('Token balances updates sent to Telegram.\n')

            else:
                print(
                    'No token balances update found, so no message sent to Telegram.\n'
                )

    print('Total time taken: {:.2f} seconds\n'.format(time.time() -
                                                            start_time))


if __name__ == "__main__":
    from urllib3.exceptions import InsecureRequestWarning
    import urllib3

    urllib3.disable_warnings(InsecureRequestWarning)

    parser = argparse.ArgumentParser(
        description="Get parameters for the script.")
    parser.add_argument('-c',
                        '--chat',
                        type=str,
                        default='GROUP',
                        help="GROUP: Send to TEST_TG_CHAT_ID Telegram group, \
                                USER: Send to USER_ID Telegram user")
    parser.add_argument('-m',
                        '--mode',
                        type=str,
                        default='NEW',
                        help="NEW: Output only new coins, \
                                NORMAL: Output all coins with balances change")
    args = parser.parse_args()
    chat = str(args.chat).upper()
    mode = str(args.mode).upper()

    if chat not in ['GROUP', 'USER']:
        print(
            "\nChat {} is not supported. Supported options are GROUP and USER.\n"
            .format(chat))
        sys.exit(1)
    elif chat == 'GROUP':
        chat_id = TEST_TG_CHAT_ID
    else:
        chat_id = USER_ID

    if mode not in ['NEW', 'NORMAL']:
        print(
            "\nMode {} is not supported. Supported options are NEW and NORMAL.\n"
            .format(mode))
        sys.exit(1)

    get_token_balance_change(mode, chat_id, logger)
