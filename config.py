import os
from configparser import ConfigParser

root_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(root_dir, "private.ini")
cfg = ConfigParser()

if os.path.exists(config_file):
    cfg.read(config_file)
else:
    cfg = None

if cfg:
    if cfg.has_section('bitquery'):
        bitquery = dict(cfg.items('bitquery'))
        BITQUERY_CLIENT_ID = bitquery.get('bitquery_client_id', '')
        BITQUERY_CLIENT_SECRET = bitquery.get('bitquery_client_secret', '')
        BITQUERY_V1_API_KEY = bitquery.get('bitquery_v1_api_key', '')
    else:
        BITQUERY_CLIENT_ID = ''
        BITQUERY_CLIENT_SECRET = ''
        BITQUERY_V1_API_KEY = ''

    if cfg.has_section('vybe_network'):
        vybe_network = dict(cfg.items('vybe_network'))
        cleaned_keys = vybe_network.get('vybe_network_x_api_keys',
                                        '').replace("\\\n", "")
        VYBE_NETWORK_X_API_KEYS = [
            item.strip() for item in cleaned_keys.split(",")
        ]
    else:
        VYBE_NETWORK_X_API_KEYS = ['']

    if cfg.has_section('telegram'):
        telegram = dict(cfg.items('telegram'))
        TELEGRAM_BOT_TOKEN = telegram.get('telegram_bot_token', '')
        TEST_TG_CHAT_ID = telegram.get('test_tg_chat_id', '')
        USER_ID = telegram.get('user_id', '')
    else:
        TELEGRAM_BOT_TOKEN = ''
        TEST_TG_CHAT_ID = ''
        USER_ID = ''

    if cfg.has_section('vercel'):
        vercel = dict(cfg.items('vercel'))
        VERCEL_APP_URL = vercel.get('vercel_app_url', '')
    else:
        VERCEL_APP_URL = ''
else:
    BITQUERY_CLIENT_ID = ''
    BITQUERY_CLIENT_SECRET = ''
    BITQUERY_V1_API_KEY = ''
    VYBE_NETWORK_X_API_KEYS = ['']
    TELEGRAM_BOT_TOKEN = ''
    TEST_TG_CHAT_ID = ''
    USER_ID = ''
    VERCEL_APP_URL = ''

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
    "CNvitvFnSM5ed6K28RUNSaAjqqz5tX1rA5HgaBN9pump",  # FRED
    "DwDtUqBZJtbRpdjsFw3N7YKB5epocSru25BGcVhfcYtg",  # WORM
    "A8C3xuqscfmyLrte3VmTqrAq8kgMASius9AFNANwpump",  # FWOG
    "H2c31USxu35MDkBrGph8pUDUnmzo2e4Rf4hnvL2Upump",  # Shoggoth
    "63LfDmNb3MQ8mw9MtZ2To9bEA2M71kZUUGq5tiJxcqj9",  # GIGA
    "5SVG3T9CNQsm2kEwzbRq6hASqh1oGfjqTtLXYUibpump",  # SIGMA
    "DPaQfq5sFnoqw2Sh9WMmmASFL9LNu6RdtDqwE1tab2tB",  # SKBDI
    "Df6yfrKC8kZE3KNkrHERKzAetSxbrWeniQfyJY4Jpump",  # CHILLGUY
    "9psiRdn9cXYVps4F1kFuoNjd2EtmqNJXrCPmRppJpump",  # UBC
    "79yTpy8uwmAkrdgZdq6ZSBTvxKsgPrNqTLvYQBh1pump",  # BULLY
    "FQ1tyso61AH1tzodyJfSwmzsD3GToybbRNoZxUBz21p8",  # VVAIFU
    "GmbC2HgWpHpq9SHnmEXZNT5e1zgcU9oASDqbAkGTpump",  # CATANA
    "DDij7Dp8updt3XSCzeHCaAoDoFTSE5Y27i2EQ9qjMQtr",  # RURI
    "9qriMjPPAJTMCtfQnz7Mo9BsV2jAWTr2ff7yc3JWpump",  #  
    "6b7NtVRo6jDSUZ75qfhHgpy99XVkSu1kfoTFu2E3pump",  # PRAWN
    "4BBjpGwLgGmUxtT82YFK9xMhcvyy3zgf3HpxTRip1YoU",  # Mundi
    "Gu3LDkn7Vx3bmCzLafYNKcDxv2mH7YN44NJZFXnypump",  # DEGENAI
    "GfVkzaeEmgfP51zSESJydGmtFheud37LeQfm9WQ3pump",  # QWEN 
    "HNg5PYJmtqcmzXrv6S9zP1CDKk5BgDuyFBxbvNApump",  # ALCH
]

WALLET_ADDRESSES_TO_INCLUDE = [
    "nPosUpnDtaB4dBaJUMF1bm78E4BTZDwWQWGoEmEyESx",  # $QWEN early buyer
    "H3ULqKdSDvXAz1UKQYyfauoak7ZF8ubjQtL6yPKxLVn9",  # $QWEN early buyer
    "BZmxuXQ68QeZABbDFSzveHyrXCv5EG6Ut1ATw5qZgm2Q",  # $QWEN early buyer
    "3PXphc83oYA6T9Xzi3c1q8ENQCSVRX1vofBJvQFGSU3P",  # PRAWN early buyer
    "CYjF5avYZmEhC1DJyZfR9rKEYB2qNakAfxL4LKHW91Kh",  # PRAWN early buyer
    "H6RErn6vTw3ZSLBN9iNpP3cAq8CETh6dy6HVkEwPonjE",  # CHILLGUY early buyer
    "8WXKcUjwMU5TxiEN4mjw52iP4uPKx8VpXGozqMadqhyq",  # CHILLGUY early buyer
    "3dzy3JJzfS882FsQvhLtoH7EVJhLM23UnMzb1movjeaM",  # CHILLGUY early buyer
    "DFTvt9LdKLKVuLjXxyFsP2W7WQwDnawgpqUz5f6gkfxj",  # CHILLGUY early buyer
    "928HvrAk5YVgksEP87KixnkhqjXTcagYYmZfZzSgLq8T",  # CHILLGUY early buyer
    "4GwjiXRfCerHjrf7fjPPsewLMTu3gN7pMnkA3bGcANT3",  # CHILLGUY early buyer
    "HfqgVXrKv8vBoqLGqGgEpxAR1vw6hUH28CUkdytU2Cuf",  # CHILLGUY early buyer
    "FWuPsvShrLG4r6iYjc3dDCoPneHFdYqDGX4MXuhTDf6y",  # CHILLGUY early buyer
    "799w4dfUDCLSvTynuWAB67rEmugUW68ZZzKUgr5k6isR",  # CHILLGUY early buyer
    "5dDDSix4JDnGGRYxntQKpbnWzMyedu9euxy4Jc8D44yF",  # CHILLGUY early buyer
    "68MbxgnxADFnkijppvw3dTPu3NRCiAYGtCCrkhUTUPfb",  # CHILLGUY early buyer
    "6bVLiHHZUQnj5UsqMh9zTme7pzPLm4cVdnzkThQz5SRP",  # CHILLGUY early buyer
    "2GTxgLAsbHPGUWSuj7n2kb7JpW2xQhzfXv3ukqpEjdDi",  # CHILLGUY early buyer
    "2cyYy2zPyThCJAVcD4JhqnTWnsTVSVJe55Gw3NrPKBf8",  # RIF early buyer
    "8RZdvcLRn6Cg9W2RnLiXAv8vxBujfEignbB2Nagoo1Lj",  # URO early buyer
    "5mUat7qeNwrGPmWzHCJ1Lnw5eXXJhpq25zPHWMtZQaRy",  # ZEREBRO early buyer
    "GB4PGoxJ5qaxmkdfBCxhw5Pcfet5Y5CpeMXdPwyBoj2R",  # ZEREBRO early buyer
    "6MxgUd3C45Dmxr9qKKq6hpMiR6gFsziuDHRRDk5JK53L",  # ZEREBRO early buyer
    "D8YvsyB39r1Crv8sYwLiZqrq5tGBUfhMv6nNBcaBbhVe",  # ZEREBRO early buyer
    "3U6JNL6C4nwkr2GjKunqftQR84J9e6BHcd9d969zDgbr",  # AVA early buyer
    "3TAUa4TSbxKEDTQciEUT75svJkwfUDaXw3PbeS5G9H7b",  # AVA early buyer
    "BcHJmd3QK1Z2GxjQT4zymmiixRtfogUvfHR2gQo5ErWW",  # SKBDI early buyer
    "8fF6jokXDo2f2TdV7KqHaWrxUHZV5xZbfeyBH49XQgWw",  # SKBDI early buyer
    "HeBiD5qxwbaLXP9WxNtTca7hT9czsXwz2rbi4ugtmyzd",
    "HYWo71Wk9PNDe5sBaRKazPnVyGnQDiwgXCFKvgAQ1ENp",  # MOODENG whale
    "71m12A5zLEowFRkwunLvd1MgUUPRBbMCxQPafxkg9idF",  # insider
    "xwgpZSfJfqDBW2UL7eSaQmcWx6JrFcCjXAvZqR7tfdr",  # insider
    "j1oeQoPeuEDmjvyMwBmCWexzCQup77kbKKxV59CnYbd",  # insider
    "FkZwrAbE7Zze4NdqcFVTXhM9fktyfzQ5Ufp8K7v2H6gY",  # MICHI top holder
    "GednEH4dgpdvTdUgDNHg4BAHLa5KPQojbcHSF6eg38JB",
    "HooderpigTVYapoXi6PQzxwtWhq3U1cuGvyu89fGjruY",
    "Bqf76TrvZr637xvei14mHr1odxBTvKQccBYXhxJjp2RT",
    "8icKqfmu95pCmfQLc2cLkmhB7LqN8tRaaE4cvKnGpwpq",
    "Baoy8GbXcwP1VWmwZDnwFTsm5BedkxJTZydJ2rvZAHYu",
    "9UWZFoiCHeYRLmzmDJhdMrP7wgrTw7DMSpPiT2eHgJHe",
    "DfMxre4cKmvogbLrPigxmibVTTQDuzjdXojWzjCXXhzj",
    "CNudZYFgpbT26fidsiNrWfHeGTBMMeVWqruZXsEkcUPc",
    "4Be9CvxqHW6BYiRAxW9Q3xu1ycTMWaL5z8NX4HR3ha7t",
    "3vWJYyyGYJzudZFjYWVMPLCFCuKnhSab6oDboD8WggBv",
    "J7pcdtNbbjDWzz4k438aca3aUciq5PogbnMW4FpmZjJj",
    "Ca1DdGgk1S8GAWsPAWGYG5ufafUofjGwutvt9cNRiW71",
    "5sTQ5ih7xtctBhMXHr3f1aWdaXazWrWfoehqWdqWnTFP",
    "jz1RPBQEEgroa63tqPfNWDUgEoJbDzLgz3TthDMHbB1",
    "Hwz4dFRbEbUTeY4oxVXyQrxXdBtvqdGRH3qcgvYu7fs8",
    "HVh6wHNBAsG3pq1Bj5oCzRjoWKVogEDHwUHkRz3ekFgt",
    "AcUm7PunTqCYnLKD5ZbXaA4VtrWd8jccwPFCY3yMvLRa",
    "5PAhQiYdLBd6SVdjzBQDxUAEFyDdF5ExNPQfcscnPRj5",
    "8Hkbb3fkyBZi92dtGEXWuZyErRhUHSnHwTQJjxr32upg",
    "8e2CGqUwRSTc6KW6a5PkTL4CQmkemdc86x7xWumdqiR",
    "H1Tw7sVRuaSZTcWhEbCuKwFMSxUmqWRWmX1PLW1HxQ2B",
    "4PstEU8cBCGG82B9cXuAXWqndzCgvD7KAGBDTvyKJ9SV",
    "BQaNx1LdG7YsM5FNCHYszCDSeoXXEmjTgvaQzLngBuG4",
    "GpNbukV5nggkJfsEEbKrJaZkdgYcNWCAaD91Mi4MmGQi",
    "EoN2ef1hPAT9WCw6gjkgp6922WvagdCcjkJGkXqB33aW",
    "AM84n1iLdxgVTAyENBcLdjXoyvjentTbu5Q6EpKV1PeG",
    "3h65MmPZksoKKyEpEjnWU2Yk2iYT5oZDNitGy5cTaxoE",
    "6pZYNHDpntcCxogx7gs5aVbTJGLDPZKCW3Nm8qV7BeBD",
    "9U9ojKpGc65PT6vfzQVKsP53UNaaTiwgzjDUYcDNRywZ",
    "4t9bWuZsXXKGMgmd96nFD4KWxyPNTsPm4q9jEMH4jD2i",
    "71CPXu3TvH3iUKaY1bNkAAow24k6tjH473SsKprQBABC",
    "8rkW2bDcurENSYaEhLBpZ1eSiJBy1bfSTrmHtrTcKqjT",  # OUTER early buyer, possibly @Weeb_Mcgee
    "CjUSBD8PktVf5SVbjGQKvnMF3wHZEhQFzV2VCRGT2oQG",  # JUSTIN early buyer
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
EPSILON = 1e-4
MIN_MARKETCAP = 1e5
