import os
from configparser import ConfigParser

root_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(root_dir, "private.ini")
cfg = ConfigParser()
cfg.read(config_file)

bitquery = dict(cfg.items('bitquery'))
BITQUERY_CLIENT_ID = bitquery.get('bitquery_client_id', '')
BITQUERY_CLIENT_SECRET = bitquery.get('bitquery_client_secret', '')
BITQUERY_V1_API_KEY = bitquery.get('bitquery_v1_api_key', '')

vybe_network = dict(cfg.items('vybe_network'))
VYBE_NETWORK_X_API_KEY = vybe_network.get('vybe_network_x_api_key', '')

BITQUERY_API_VERSION = 'EAP'
BITQUERY_API_VERSION_URL_MAP = {
    'v1': 'https://graphql.bitquery.io/',
    'v2': 'https://streaming.bitquery.io/graphql',
    'EAP': 'https://streaming.bitquery.io/eap',
}

MINT_ADDRESSES = [
    "ED5nyyWEzpPPiWimP8vYm7sD7TD3LAt3Q3gRTWHzPJBY",  # MOODENG
    "GtDZKAqvMZMnti46ZewMiXCa4oXF4bZxwQPoKzXPFxZn",  # NUB
    "GJtJuWD9qYcCkrwMBmtY1tpapV1sKfB2zUv9Q4aqpump",  # RIF
    "FvgqHMfL9yn39V79huDPy3YUNDoYJpuLWng2JfmQpump",  # URO
    "2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump",  # PNUT
    "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",  # ai16z
    "CBdCxKo9QavR9hfShgpEBG3zekorAeD7W1jfq2o3pump",  # LUCE
    "8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn",  # ZEREBRO
    "DKu9kykSfbN5LBfFXtNNDPaX35o4Fv6vJ9FKk7pZpump",  # AVA
    "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump",  # GOAT
    "FLqmVrv6cp7icjobpRMQJMEyjF3kF84QmC4HXpySpump",  # BUCK
    "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump",  # Fartcoin
    "HwPtbFpd3VTe3tfyosoVtPf9WPuSk5gAKkN5xp6Npump",  # 🟥🟩
    "CNvitvFnSM5ed6K28RUNSaAjqqz5tX1rA5HgaBN9pump",  # FRED
    "DwDtUqBZJtbRpdjsFw3N7YKB5epocSru25BGcVhfcYtg",  # WORM
    "A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump",  # FWOG
    "H2c31USxu35MDkBrGph8pUDUnmzo2e4Rf4hnvL2Upump",  # Shoggoth
    "63LfDmNb3MQ8mw9MtZ2To9bEA2M71kZUUGq5tiJxcqj9",  # GIGA
    "5SVG3T9CNQsm2kEwzbRq6hASqh1oGfjqTtLXYUibpump",  # SIGMA
    "DPaQfq5sFnoqw2Sh9WMmmASFL9LNu6RdtDqwE1tab2tB",  # SKBDI
    "Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump",  # CHILLGUY
]

EXCLUDED_ADDRESSES = {
    "BQ72nSv9f3PRyRKCBnHLVrerrv37CYTHm5h3s9VSGQDV":
    True,  # Jupiter Aggregator Authority 1
    "2MFoS3MPtvyQ4Wh4M9pdfPjz6UhVoNbFbGJAskCPCj3h":
    True,  # Jupiter Aggregator Authority 2
    "HU23r7UoZbqTUuh3vA7emAGztFtqwTeVips789vqxxBw":
    True,  # Jupiter Aggregator Authority 3
    "3CgvbiM3op4vjrrjH2zcrQUwsqh5veNVRjFCB9N6sRoD":
    True,  # Jupiter Aggregator Authority 4
    "6LXutJvKUw8Q5ue2gCgKHQdAN4suWW8awzFVC6XCguFx":
    True,  # Jupiter Aggregator Authority 5
    "CapuXNQoDviLvU1PxFiizLgPNQCxrsag1uMeyk6zLVps":
    True,  # Jupiter Aggregator Authority 6
    "GGztQqQ6pCPaJQnNpXBgELr5cs3WwDakRbh1iEMzjgSJ":
    True,  # Jupiter Aggregator Authority 7
    "9nnLbotNTcUhvbrsA6Mdkx45Sm82G35zo28AqUvjExn8":
    True,  # Jupiter Aggregator Authority 8
    "3LoAYHuSd7Gh8d7RTFnhvYtiTiefdZ5ByamU42vkzd76":
    True,  # Jupiter Aggregator Authority 9
    "DSN3j1ykL3obAVNv7ZX49VsFCPe4LqzxHnmtLiPwY6xg":
    True,  # Jupiter Aggregator Authority 10
    "69yhtoJR4JYPPABZcSNkzuqbaFbwHsCkja1sP1Q2aVT5":
    True,  # Jupiter Aggregator Authority 11
    "6U91aKa8pmMxkJwBCfPTmUEfZi6dHe7DcFq2ALvB2tbB":
    True,  # Jupiter Aggregator Authority 12
    "7iWnBRRhBCiNXXPhqiGzvvBkKrvFSWqqmxRyu9VyYBxE":
    True,  # Jupiter Aggregator Authority 13
    "4xDsmeTWPNjgSVSS1VTfzFq3iHZhp77ffPkAmkZkdu71":
    True,  # Jupiter Aggregator Authority 14
    "GP8StUXNYSZjPikyRsvkTbvRV1GBxMErb59cpeCJnDf1":
    True,  # Jupiter Aggregator Authority 15
    "HFqp6ErWHY6Uzhj8rFyjYuDya2mXUpYEk8VW75K9PSiY":
    True,  # Jupiter Aggregator Authority 16
}

variables = {}

MAX_RETRIES = 10
RETRY_AFTER = 10
EDGE_POINTS_QUANTITY = 100
EDGE_POINTS_OPACITY = 0
VYBE_NETWORK_QUERY_LIMIT = 1000
