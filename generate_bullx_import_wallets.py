import string
from utils import *
from config import WALLET_ADDRESSES_TO_INCLUDE_DICT

def generate_unique_emoji_sequential(existing_emojis):
    emoji_blocks = list(range(0x1F300, 0x1F5FF + 1)) + list(range(0x1F600, 0x1F64F + 1)) + list(range(0x1F680, 0x1F6FF + 1)) + list(range(0x1F900, 0x1F9FF + 1))
    for code_point in emoji_blocks:
        emoji = chr(code_point)
        if emoji not in existing_emojis:
            existing_emojis.add(emoji)
            return emoji
    raise ValueError("Ran out of unique emojis!")

def convert_wallet_dict_to_list(wallet_dict):
    existing_emojis = set()
    result = []
    for address, label in wallet_dict.items():
        emoji = generate_unique_emoji_sequential(existing_emojis)
        result.append({
            'name': label,
            'address': address,
            'emoji': emoji,
            'tags': []
        })
    return result

converted_list = convert_wallet_dict_to_list(WALLET_ADDRESSES_TO_INCLUDE_DICT)

saved_data_base_dir = "./saved_data"
bullx_import_wallets_dir = saved_data_base_dir + "/bullx_import_wallets"
os.makedirs(bullx_import_wallets_dir, exist_ok=True)
bullx_import_wallets_file_path = f"{bullx_import_wallets_dir}/bullx_import_wallets.json"

if os.path.exists(bullx_import_wallets_file_path):
    os.remove(bullx_import_wallets_file_path)
save_json_file(bullx_import_wallets_file_path,
                converted_list)
