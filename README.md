# memecoins_trading_toolkit

# Token Balance Tracker and Update System

This repository contains a Python script designed to monitor and update the token balances of top trader wallets, including tracking token changes, querying token data from Vybe Network, and integrating with Telegram for notifications.

## Overview

The script retrieves token balance information for a list of top trader wallets, calculates token balance changes (additions and subtractions), and updates a local database. Additionally, it fetches token details from DexScreener and analyzes trends related to tokens using Google Trends.

## Features

- Queries Vybe Network's API for token balances of specified wallet addresses.
- Tracks changes in token balances (both additions and subtractions).
- Saves the updated token balances and tracked changes in a local JSON file.
- Filters tokens based on market capitalization (with a minimum threshold).
- Retrieves additional token details from DexScreener.
- Integrates with Google Trends to analyze the interest in tokens.
- Sends Telegram notifications with detailed information about token balance updates.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/token-balance-tracker.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

In the `config.py` file, configure the following:

- `VYBE_NETWORK_X_API_KEYS`: List of API keys for accessing Vybe Network's API.
- `VYBE_NETWORK_QUERY_LIMIT`: The limit for the number of token balances to query per request.
- `MAX_RETRIES`: Maximum number of retries in case of API failures.
- `RETRY_AFTER`: Delay in seconds before retrying a failed request.
- `MIN_MARKETCAP`: Minimum market cap for filtering tokens to be included in updates.
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `USER_ID`: Your Telegram user ID to receive notifications.
- `TEST_TG_CHAT_ID`: A test chat ID for Telegram notifications.
- `MIN_BUY_AMOUNT_USD`: Minimum USD value for token buys to trigger a notification.
- `MIN_SELL_AMOUNT_USD`: Minimum USD value for token sells to trigger a notification.
- `RECENT_N_DAYS_INTEREST`: The number of days for recent trends to consider in Google Trends.

### Additional Setup

1. Rename the `private_temp.ini` file to `private.ini`.
2. Fill in the following details in the `private.ini` file:

```ini
[bitquery]
BITQUERY_CLIENT_ID = 
BITQUERY_CLIENT_SECRET = 
BITQUERY_V1_API_KEY = 

[vybe_network]
VYBE_NETWORK_X_API_KEYS = <Key 1>, \
                          <Key 2>, \
                          ...

[telegram]
TELEGRAM_BOT_TOKEN = 
TEST_TG_CHAT_ID = 
USER_ID = 

[vercel]
VERCEL_APP_URL = 
```

## Usage

Run the script with the desired mode (`NEW` or `UPDATE`) to either track new token balance changes or update existing data.

```bash
python token_balance_tracker.py --mode NEW
```

### Command-line Arguments:

- `--mode`: Specifies the mode of operation. Options are `NEW` (to output only new tokens) or `UPDATE` (to output all changes).

## Telegram Notifications

The script integrates with Telegram, sending notifications to your Telegram bot with details on token balance updates. Ensure your bot is correctly set up and the bot token is provided in the configuration.
