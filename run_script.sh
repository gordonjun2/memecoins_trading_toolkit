#!/bin/bash

# Redirect all output (stdout and stderr) to a log file
exec > >(tee -a /root/memecoins_trading_toolkit/script_output.log) 2>&1

echo "Starting script at $(date)" # Log the start time
cd /root/memecoins_trading_toolkit || { echo "Failed to change directory"; exit 1; }
echo "Changed to directory: $(pwd)"

source venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }
echo "Activated virtual environment"

echo "Running Python script"
python get_token_balances_change.py || { echo "Python script failed"; exit 1; }

echo "Script finished at $(date)"

