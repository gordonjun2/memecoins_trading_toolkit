import requests
from config import TELEGRAM_BOT_TOKEN

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"

response = requests.get(url)

if response.status_code == 200:
    print("Webhook deleted successfully!")
else:
    print(f"Failed to delete webhook: {response.text}")
