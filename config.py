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
    "HNg5PYJmtqcmzXrv6S9zP1CDKk5BgDuyFBxbvNApump",   # ALCH
    "eL5fUxj2J4CiQsmW85k5FG9DvuQjjUoBHoQBi2Kpump",   # UFD
    "GAMwtMB6onAvBNBQJCJFuxoaqfPH8uCQ2dewNMVVpump",  # TANK
]

WALLET_ADDRESSES_TO_INCLUDE_DICT = {
    'nPosUpnDtaB4dBaJUMF1bm78E4BTZDwWQWGoEmEyESx': 'nPos...yESx (Winrate: 50.00%, Tokens Traded: > 240)', 
    '3PXphc83oYA6T9Xzi3c1q8ENQCSVRX1vofBJvQFGSU3P': '3PXp...SU3P (Winrate: 27.57%, Tokens Traded: > 300)', 
    '4GwjiXRfCerHjrf7fjPPsewLMTu3gN7pMnkA3bGcANT3': '4Gwj...ANT3 (Winrate: 44.44%, Tokens Traded: > 10)', 
    'HYWo71Wk9PNDe5sBaRKazPnVyGnQDiwgXCFKvgAQ1ENp': 'HYWo...1ENp (Winrate: 31.43%, Tokens Traded: > 210)', 
    'FkZwrAbE7Zze4NdqcFVTXhM9fktyfzQ5Ufp8K7v2H6gY': 'FkZw...H6gY (Winrate: 27.61%, Tokens Traded: > 130)', 
    'GednEH4dgpdvTdUgDNHg4BAHLa5KPQojbcHSF6eg38JB': 'Gedn...38JB (Winrate: 31.43%, Tokens Traded: > 30)', 
    '9UWZFoiCHeYRLmzmDJhdMrP7wgrTw7DMSpPiT2eHgJHe': '9UWZ...gJHe (Winrate: 63.90%, Tokens Traded: > 240)', 
    'DfMxre4cKmvogbLrPigxmibVTTQDuzjdXojWzjCXXhzj': 'DfMx...Xhzj (Winrate: 87.21%, Tokens Traded: > 1570)', 
    'CNudZYFgpbT26fidsiNrWfHeGTBMMeVWqruZXsEkcUPc': 'Cnud...cUPc (Winrate: 92.31%, Tokens Traded: > 10)', 
    'J7pcdtNbbjDWzz4k438aca3aUciq5PogbnMW4FpmZjJj': 'J7pc...ZjJj (Winrate: 48.65%, Tokens Traded: > 30)', 
    'AcUm7PunTqCYnLKD5ZbXaA4VtrWd8jccwPFCY3yMvLRa': 'AcUm...vLRa (Winrate: 95.56%, Tokens Traded: > 90)', 
    '8Hkbb3fkyBZi92dtGEXWuZyErRhUHSnHwTQJjxr32upg': '8Hkb...2upg (Winrate: 60.00%, Tokens Traded: > 5)', 
    'GpNbukV5nggkJfsEEbKrJaZkdgYcNWCAaD91Mi4MmGQi': 'GpNb...mGQi (Winrate: 20.00%, Tokens Traded: > 10)', 
    '3h65MmPZksoKKyEpEjnWU2Yk2iYT5oZDNitGy5cTaxoE': '3h65...axoE (Winrate: 27.73%, Tokens Traded: > 930)', 
    '6pZYNHDpntcCxogx7gs5aVbTJGLDPZKCW3Nm8qV7BeBD': '6pZY...BeBD (Winrate: 61.54%, Tokens Traded: > 10)', 
    '9U9ojKpGc65PT6vfzQVKsP53UNaaTiwgzjDUYcDNRywZ': '9U9o...RywZ (Winrate: 51.68%, Tokens Traded: > 140)', 
    '4t9bWuZsXXKGMgmd96nFD4KWxyPNTsPm4q9jEMH4jD2i': '4t9b...jD2i (Winrate: 92.42%, Tokens Traded: > 60)', 
    '71CPXu3TvH3iUKaY1bNkAAow24k6tjH473SsKprQBABC': '71CP...BABC (Winrate: 64.06%, Tokens Traded: > 60)', 
    '8rkW2bDcurENSYaEhLBpZ1eSiJBy1bfSTrmHtrTcKqjT': '8rkW...KqjT (Winrate: 68.42%, Tokens Traded: > 10)', 
    '41U2ri3RLHHjdcyii4qENuvKGP9nD6r4U3EuaXsTMfJU': '41U2...MfJU (Winrate: 57.89%, Tokens Traded: > 30)', 
    '9c4kWxhCyLRxYi38fDcQpktqWWA44nxE5syedUsN1hr7': '9c4k...1hr7 (Winrate: 100.00%, Tokens Traded: > 0)', 
    'ANqwRG7pyjhsQTzxfNGU3K14DQnmK2U6r6CoqjyoJC8R': 'Anqw...JC8R (Winrate: 40.09%, Tokens Traded: > 220)', 
    'hJRWEXNPGcjvYyPqttHC4Fba3ZeNDBFkb15E32EwhAR': 'hJRW...whAR (Winrate: 27.72%, Tokens Traded: > 100)', 
    'H7WkwWrQWTLNJfJhqjNV2DGM6hXxmvSBv7vEchQKa1ys': 'H7Wk...a1ys (Winrate: 21.17%, Tokens Traded: > 130)', 
    'BJ7xvzDbcsX1JdgnLhwesnKB9pSjZWdCgbW9JBXB3qXa': 'BJ7x...3qXa (Winrate: 35.14%, Tokens Traded: > 30)', 
    'F8nt7vqkFrYbjPdRkKwuZGXoWZWX6Yg3vKdEX8TfvVY7': 'F8nt...vVY7 (Winrate: 48.76%, Tokens Traded: > 120)', 
    '82kLuMXSns4aecHQoDm88g5v9sCzdhW2yiaQBoGvdxvm': '82kL...dxvm (Winrate: 69.23%, Tokens Traded: > 30)', 
    '2Qt3jug4PNJuiGKx2XR7Bs3bk1nX8v9hArzCzkYABk1o': '2Qt3...Bk1o (Winrate: 41.67%, Tokens Traded: > 10)', 
    'Hqkk2zNPZYiQL7c9JhVed1EyQppoZToBKMCzaCX1m21y': 'Hqkk...m21y (Winrate: 27.11%, Tokens Traded: > 500)', 
    '215nhcAHjQQGgwpQSJQ7zR26etbjjtVdW74NLzwEgQjP': '215n...gQjP (Winrate: 30.56%, Tokens Traded: > 580)', 
    '5pRpKmNNskgSzeJ6S7Pr6KEHuLpBbQAgjKH74pMn1q62': '5pRp...1q62 (Winrate: 41.94%, Tokens Traded: > 180)', 
    'M5Q1hFKopMr2DyNabEkrgoh6tGaF6z6NVQZ5SGUPss8': 'M5Q1...Pss8 (Winrate: 32.89%, Tokens Traded: > 750)', 
    '5X4593sntQAyxwciqC87mdyZqVVk1Y9ydUPVUF9nUq7T': '5X45...Uq7T (Winrate: 23.81%, Tokens Traded: > 40)', 
    'CLegS2MSiCsBksVazCg4Y7Gz3NqeBK21QyvzK4Q7S168': 'CLeg...S168 (Winrate: 30.59%, Tokens Traded: > 80)', 
    'DXSWECvcdajmyHhnSYaVKTXd28vFPgoDXTs1P2ppXoNX': 'DXSW...XoNX (Winrate: 51.67%, Tokens Traded: > 180)', 
    '687kTFNvKG9GXf8UsPzyrKbKpz5ExNrSCWfs7S4PTGiL': '687k...TGiL (Winrate: 46.71%, Tokens Traded: > 330)', 
    'ACHhRQMbTxuWqU3bmbBbgUNGsPsYnvB8KLcPkkXCY1C7': 'ACHh...Y1C7 (Winrate: 40.82%, Tokens Traded: > 40)', 
    'CLpDttr14kM4svu7jypK4rzsMKdJYAR8emGNPaWs7omB': 'CLpD...7omB (Winrate: 37.93%, Tokens Traded: > 170)', 
    'Fqgsp9CziV5DhyseYahkbFWLPFwFKsMyoK3abEjauw6Y': 'Fqgs...uw6Y (Winrate: 48.15%, Tokens Traded: > 180)', 
    '9AgRdvmNSgtyiKf6dYsBCPJDEXG6pNWKXswZabndYf7v': '9AgR...Yf7v (Winrate: 41.99%, Tokens Traded: > 1590)', 
    '8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd': '8zFZ...c7Zd (Winrate: 45.54%, Tokens Traded: > 100)', 
    '2ssNnQ777XH4JZktYq6dh6bcMz5xdwP89pzTLPpEPkzK': '2ssN...PkzK (Winrate: 38.74%, Tokens Traded: > 300)', 
    'HdxkiXqeN6qpK2YbG51W23QSWj3Yygc1eEk2zwmKJExp': 'Hdxk...Jexp (Winrate: 47.42%, Tokens Traded: > 980)', 
    'ApH45VZp3bhgGeFb2UBHTymxkjsGvNbrfAybd8TfXQLu': 'ApH4...XQLu (Winrate: 49.28%, Tokens Traded: > 60)', 
    '2DVbzAaaxyYUZJnYmmqfUned3t5SWVPZpFfrQcUvVnxW': '2DVb...VnxW (Winrate: 22.01%, Tokens Traded: > 300)', 
    'BvpqgSpMAB1KmasdsTij52KZdSCPy87QMXypDy2b4n2R': 'Bvpq...4n2R (Winrate: 28.72%, Tokens Traded: > 90)', 
    '6KVyzB7Sxx2Rnk7J8ZEhBZPbKyiRq3tPY9YNhtCjcems': '6KVy...cems (Winrate: 25.81%, Tokens Traded: > 30)', 
    '8sHfJ1WTV3HsfDJwRHtiseMsBHVrE5qNNrZgSYswxpgv': '8sHf...xpgv (Winrate: 33.02%, Tokens Traded: > 840)', 
    'Ay9wnuZCRTceZJuRpGZnuwYZuWdsviM4cMiCwFoSQiPH': 'Ay9w...QiPH (Winrate: 36.09%, Tokens Traded: > 230)', 
    'AbcX4XBm7DJ3i9p29i6sU8WLmiW4FWY5tiwB9D6UBbcE': 'AbcX...BbcE (Winrate: 63.63%, Tokens Traded: > 180)', 
    'FvUPaRvw86WugTBPCSJ2xdYatKn86FB17ThDwGc9D8Bj': 'FvUP...D8Bj (Winrate: 22.69%, Tokens Traded: > 1080)', 
    'BZmxuXQ68QeZABbDFSzveHyrXCv5EG6Ut1ATw5qZgm2Q': 'BZmx...gm2Q (Winrate: 27.05%, Tokens Traded: > 120)', 
    'FWuPsvShrLG4r6iYjc3dDCoPneHFdYqDGX4MXuhTDf6y': 'FwuP...Df6y (Winrate: 36.51%, Tokens Traded: > 60)', 
    '2cyYy2zPyThCJAVcD4JhqnTWnsTVSVJe55Gw3NrPKBf8': '2cyY...KBf8 (Winrate: 44.44%, Tokens Traded: > 0)',
    '2cqm3UDc7dh3EkkKeuQWDSdDBHuBY55W8ynHxy5ga3d2': '2cqm...a3d2 (Winrate: 87.67%, Tokens Traded: > 70)', 
    '831qmkeGhfL8YpcXuhrug6nHj1YdK3aXMDQUCo85Auh1': '831q...Auh1 (Winrate: 77.12%, Tokens Traded: > 150)', 
    'DjNjRmjMBso49J7sfJKH1rSS8pEvBMJk6ABFX7tNABWH': 'DjNj...ABWH (Winrate: 77.94%, Tokens Traded: > 60)', 
    '5q7Xwc2T57sK1DKU6zuwVXvMPsxqB2xrJ3T5AonFYtcY': '5q7X...YtcY (Winrate: 83.95%, Tokens Traded: > 160)', 
    '2RssnB7hcrnBEx55hXMKT1E7gN27g9ecQFbbCc5Zjajq': '2Rss...jajq (Winrate: 82.95%, Tokens Traded: > 350)', 
    '2CXbN6nuTTb4vCrtYM89SfQHMMKGPAW4mvFe6Ht4Yo6z': '2CXb...Yo6z (Winrate: 82.42%, Tokens Traded: > 450)', 
    'CRVidEDtEUTYZisCxBZkpELzhQc9eauMLR3FWg74tReL': 'CRVi...tReL (Winrate: 28.17%, Tokens Traded: > 1380)', 
    'ApRnQN2HkbCn7W2WWiT2FEKvuKJp9LugRyAE1a9Hdz1': 'ApRn...Hdz1 (Winrate: 62.93%, Tokens Traded: > 370)', 
    'HLv6yCEpgjQV9PcKsvJpem8ESyULTyh9HjHn9CtqSek1': 'HLv6...Sek1 (Winrate: 70.59%, Tokens Traded: > 10)', 
    'Hvts7WUNA9k72kkVt2YP6z1R85U3C637XqfCNoaYSy3W': 'Hvts...Sy3W (Winrate: 50.47%, Tokens Traded: > 100)', 
    '8rvAsDKeAcEjEkiZMug9k8v1y8mW6gQQiMobd89Uy7qR': '8rvA...y7qR (Winrate: 47.96%, Tokens Traded: > 1670)', 
    '4q7rNU1nRUWY14vaLPpzpc2C756UQE36vaDwphBpLf2s': '4q7r...Lf2s (Winrate: 36.71%, Tokens Traded: > 310)', 
    'HdxkiXqeN6qpK2YbG51W23QSWj3Yygc1eEk2zwmKJExp': 'Hdxk...Jexp (Winrate: 43.47%, Tokens Traded: > 1070)', 
    'GeXAHmmETnizW6af4E2e64ju8mTkLdEQzxUiAjJVo6NZ': 'GeXA...o6NZ (Winrate: 38.46%, Tokens Traded: > 110)', 
    'DNfuF1L62WWyW3pNakVkyGGFzVVhj4Yr52jSmdTyeBHm': 'Dnfu...eBHm (Winrate: 93.48%, Tokens Traded: > 40)', 
    'BieeZkdnBAgNYknzo3RH2vku7FcPkFZMZmRJANh2TpW': 'Biee...2TpW (Winrate: 75.56%, Tokens Traded: > 260)', 
    '71CPXu3TvH3iUKaY1bNkAAow24k6tjH473SsKprQBABC': '71CP...BABC (Winrate: 64.06%, Tokens Traded: > 60)', 
    '8zFZHuSRuDpuAR7J6FzwyF3vKNx4CVW3DFHJerQhc7Zd': '8zFZ...c7Zd (Winrate: 45.54%, Tokens Traded: > 100)',
    '2qvsbXgfKHaNk7S6bUM2Vbhp9E73yabdzWVYtTd6xgWy': '2qvs…xgWy (Winrate: 38.32%, Tokens Traded: > 480)',
    '9wQpTf7HTSwLwtbi9m9KU43484rFPfM6AYwypa2NMzNu': '9wQp…MzNu (Winrate: 46.15%, Tokens Traded: > 20)',
    '8VZec6dMJhsAh7iPkdUoDqPtge35yn22xibonAqAEhMZ': '8VZe…EhMZ (Winrate: 28.32%, Tokens Traded: > 390)',
    'GXSnn8dApJCcNoKmBuguJY12Lo4bVLhPw1G4PdHkrCgQ': 'GXSn…rCgQ (Winrate: 27.73%, Tokens Traded: > 1120)',
    '3biFgN17V4re69LZLJNW7k8zKGjJCFjwcwAWP9z3hBLs': '3biF…hBLs (Winrate: 27.74%, Tokens Traded: > 1200)',
    'CipPqhxu4BaDM4QAhVaxEEtb2sweoRJDZ3knVrwPYEZx': 'CipP…YEZx (Winrate: 44.58%, Tokens Traded: > 80)',
    '85pLpaUF2R9SDkGYUMc69gcfo4Xa8GzUwKVg68A6UFoq': '85pL…Ufoq (Winrate: 34.77%, Tokens Traded: > 410)',
    'CmSnEzLRT53XmjSGbgbPNJmeiX3g8xP59j3t2TMc5Zce': 'CmSn…5Zce (Winrate: 26.83%, Tokens Traded: > 760)',
    'DZWRFGfm5563GBniGAUKxmBzpHoEcr12Y1rGgzqujVFU': 'DZWR…jVFU (Winrate: 42.11%, Tokens Traded: > 190)',
    '548Tz6GJZz1nC2faqQLNCpTs7JyvaPzv2fDGwD33Q7eM': '548T…Q7eM (Winrate: 35.94%, Tokens Traded: > 60)',
    'FCtfuq9CtCZ4HG4u4zhem9ZyGnb4VEDb9Swxg5frRwDD': 'FCtf…RwDD (Winrate: 31.67%, Tokens Traded: > 60)',
    'BHvUqX6mFBcgYRVwxCyh18yxgwhqq2jKQRnU6pSNvGWD': 'BHvU…vGWD (Winrate: 52.92%, Tokens Traded: > 560)',
    'iWinRYGEWcaFFqWfgjh28jnqWL72XUMmUfhADpTQaRL': 'iWin…QaRL (Winrate: 53.03%, Tokens Traded: > 260)',
    'F6n4Ha8irtGP18htXtebWeY1AqADQVmbqFFr6Xzjoq6U': 'F6n4…oq6U (Winrate: 29.10%, Tokens Traded: > 560)',
    '8sGi4W7ZQCDMgzA17eF57voRUveXyT4XPA8WTsj6HLT8': '8sGi…HLT8 (Winrate: 23.33%, Tokens Traded: > 120)',
    'F4FPCHxu19zRnSixDtCXDJC7YJTHb28n9nxZptaRq6Wp': 'F4FP…q6Wp (Winrate: 24.69%, Tokens Traded: > 80)',
    'CW6XezzEftYw4aALKo96x6oudqBZ3sfVXrfF23hAezdX': 'CW6X…ezdX (Winrate: 38.14%, Tokens Traded: > 110)',
    'EtTaTMBX9ErigazzzGmD8vq9mcwFoHrxchr2ewwzsefG': 'EtTa…sefG (Winrate: 34.14%, Tokens Traded: > 1310)',
    'BZwuFHd1sLw7bMrMWVgoVhVVQAcb5bgi1JMVFTpHmcrh': 'Bzwu...mcrh (Winrate: 22.79%, Tokens Traded: > 130)',
    '5AqbjAg3u2mSemHbmA3HPzcaTr3Xuosax4vsW3t8gPAr': '5Aqb…gPAr (Winrate: 49.49%, Tokens Traded: > 90)',
    'suqh5sHtr8HyJ7q8scBimULPkPpA557prMG47xCHQfK': 'suqh…HQfK (Winrate: 75.94%, Tokens Traded: > 7800)',
    'H6oeKZ78wouvRGVJXHioyPJuEBPh4H7UGvyxJ5rS95u1': 'H6oe…95u1 (Winrate: 25.95%, Tokens Traded: > 500)',
    '34xpG819UcgHBGXDTVn5XBQy3qYM6DFPR3tvvPwcGTMs': '34xp…GTMs (Winrate: 42.37%, Tokens Traded: > 1520)',
    '8bo92fMyMqgKD8zd83DLAp6F8nD2bCNpe3pj2aqY4QLq': '8bo9…4QLq (Winrate: 51.61%, Tokens Traded: > 30)',
    'ATmKENkRrL1JQQnoUNAQvkiwgjiHKUkzyncxTGxyzQL1': 'ATmK…zQL1 (Winrate: 45.58%, Tokens Traded: > 570)',
    '9KWS5Apsi1UBzceKvACJG5VqAE1XBA3Y8E7EER73W96a': '9KWS…W96a (Winrate: 53.85%, Tokens Traded: > 20)',
    '7dczvwnWqNE9RFe1AeECa6D9n38KN5AMiPcCWxjEVVp5': '7dcz…VVp5 (Winrate: 57.14%, Tokens Traded: > 10)',
    'EKuzYQe3J5iojMbwAeac35FgcoDvhRTSYmHYmpNpYxHc': 'Ekuz...YxHc (Winrate: 25.76%, Tokens Traded: > 60)',
    '9GaCA6ZsamjTtSrGLZ2gXfFPDVX62bU3YozzDfQJTxWF': '9GaC…TxWF (Winrate: 65.19%, Tokens Traded: > 290)',
    'c62pW6EY3gQPEpDwCW72di1bmgQaFE1z5d4yAho4pqQ': 'c62p…4pqQ (Winrate: 31.25%, Tokens Traded: > 40)',
    'CVAfeFP7PoF7qpzaeYrut7tDY2WeMHZBUYujQyasKW4f': 'CVAf…KW4f (Winrate: 30.91%, Tokens Traded: > 110)',
    'FavwU7cTsftNwXNjwfKjY26KziuasnbWD1R4xcRY4oUq': 'Favw…4oUq (Winrate: 19.35%, Tokens Traded: >30)',
    '5ea1Dy8HjvSrPgjSkLMNrwekqaWis7KCs5NUmH8e2NX8': '5ea1…2NX8 (Winrate: 26.67%, Tokens Traded: > 120)',
    '65ba3MNkbDS1DMyaS8dofX32gfTZHqGCyKhwJBMjWdg1': '65ba…Wdg1 (Winrate: 37.70%, Tokens Traded: > 510)',
    'HDU1bNyi6rBvUJNWBM1WsQgsg5dPWXtWAHgP5Bh6Acza': 'HDU1…Acza (Winrate: 26.77%, Tokens Traded: > 390)',
    'CUo3JriY1dLMWWMSvtckwMUiuLCCiADSBddm2R6idz7L': 'Cuo3…dz7L (Winrate: 48.58%, Tokens Traded: > 350)',
    'HBNHpKPQXMcf41zJPbuuJZZHqd7sJL546gEZM4jbjFuR': 'HBNH…jFuR (Winrate: 41.74%, Tokens Traded: > 350)',
    'RFSqPtn1JfavGiUD4HJsZyYXvZsycxf31hnYfbyG6iB': 'RFSq…G6iB (Winrate: 18.96%, Tokens Traded: > 570)',
    '6LbuEXvcETWtRp3gBxsy7Py8t8eAfzo4rYmpUskD9Y4t': '6Lbu…9Y4t (Winrate: 54.22%, Tokens Traded: > 160)',
    '6ryJGyrRDAcWLAmASkMVUWSX7D51pw4A3wvuYYNhQ5D8': '6ryJ…Q5D8 (Winrate: 68.16%, Tokens Traded: > 170)',
    '57JMxCescrFBvb8bqjNwHPM9J7wPF12SV5KJa82HCd9B': '57JM…Cd9B (Winrate: 36.14%, Tokens Traded: > 2300)',
    '6eQ8qJ6JJ7jx9tXKdaAX7dKtCBBZrLuUkHDSayAtXDfT': '6eQ8…XDfT (Winrate: 27.67%, Tokens Traded: > 150)',
    '9jyqFiLnruggwNn4EQwBNFXwpbLM9hrA4hV59ytyAVVz': '9jyq…AVVz (Winrate: 41.67%, Tokens Traded: > 880)',
    '5vSgQRdyY5Cti1yLRv1uQdrNFX8Eed9cBdibCDjVQbJK': '5vSg…QbJK (Winrate: 34.52%, Tokens Traded: > 80)',
    '4jgigDDym3SpE8JQwefom7WpnSv4Y5UmCKJcJ2yqPJKP': '4jgi…PJKP (Winrate: 54.12%, Tokens Traded: > 80)',
    '69JYeoEqPpQdE9dYJy6UMzW4A2eX8rA9oM1DnM7odd4G': '69JY…dd4G (Winrate: 46.49%, Tokens Traded: > 180)',
    'mW4PZB45isHmnjGkLpJvjKBzVS5NXzTJ8UDyug4gTsM': 'mW4P…gTsM (Winrate: 50.67%, Tokens Traded: > 150)',
    'ECCKBDWX3MkEcf3bULbLBb9FvrEQLsmPMFTKFpvjzqgP': 'ECCK…zqgP (Winrate: 43.91%, Tokens Traded: > 1070)',
    'BUFRTEwkvbsFUQdXxpGQWFiCoziHxnEXMFqgHqTRqF7w': 'BUFR…qF7w (Winrate: 44.91%, Tokens Traded: > 450)',
    '2QMXjBufQprAfEutzh4gMWRuMp1impcjk5BLpfYEHAsb': '2QMX…HAsb (Winrate: 75.25%, Tokens Traded: > 1210)',
    '9xivtNgqpBV1mJ9EVHyqFDvzi1DSSJvZyxaz477qr9s8': '9xiv…r9s8 (Winrate: 58.56%, Tokens Traded: > 1150)',
    'CU35ZDB4JptaBVQWiq1gZsR8kso6dz1bQj8uR3xGn2kK': 'CU35…n2kK (Winrate: 43.40%, Tokens Traded: > 580)',
    '6neoWX8Ak3wTHdFkbE487gfiK8gPnMmKWMNq9n2vzzvL': '6neo…zzvL (Winrate: 30.90%, Tokens Traded: > 280)',
    'A87rMgpBV1f48bqwguLjraq1gErgtddKkmMJ3piEQAxT': 'A87r…QAxT (Winrate: 52.23%, Tokens Traded: > 710)',
    'AVCXrniTeG4qxzumJCuNejLZ5Wx6RaSegEr1Cpctx9Fz': 'AVCX…x9Fz (Winrate: 24.24%, Tokens Traded: > 130)',
    'HUzZ1MrEUXrdPJoAnn5B8uTcshwyyXxFW1EqY2dvcVhe': 'HUzZ…cVhe (Winrate: 21.56%, Tokens Traded: > 380)',
    '5ssZC4JZKJV3V244qmMbe5Yxer6VMvEjFatnfWu2Q5YT': '5ssZ…Q5YT (Winrate: 41.77%, Tokens Traded: > 320)',
    'E4BdAz8TmRZRXRR1JBhpkxYRBnspNeyznttm6U6xPdVJ': 'E4Bd…PdVJ (Winrate: 31.37%, Tokens Traded: > 320)',
    '486Z6weq8FqFm1ywBNZXmcVgbN1odtiRfLJ6gPiTdAGs': '486Z…dAGs (Winrate: 19.57%, Tokens Traded: > 235)',
    'HEdmuuH1vTb9pND3qspVvBeSSC3eKZUeKwBDD8UaNGPe': 'Hedm...NGPe (Winrate: 66.17%, Tokens Traded: > 130)',
    '3imBHSFMXFrfQN8AFagbQs7mjJgpj7fPpsNm61RhVyKo': '3imB…VyKo (Winrate: 68.75%, Tokens Traded: > 30)',
    '4XL3h77ARiWoQAjjtWixopfXtTTEF28XAWBNy1cP6iuF': '4XL3…6iuF (Winrate: 24.35%, Tokens Traded: > 110)',
    'JDPjdakQFNHdUpr2MDU5tMows81MSdcgJh5qmUbUMFjk': 'JDPj…MFjk (Winrate: 32.99%, Tokens Traded: > 570)',
    'GCrxYNvZXhY26QtxCryGoH8nfJaiE7qGGpvh61FAui8J': 'GCrx…ui8J (Winrate: 46.99%, Tokens Traded: > 160)',
    'HUpPyLU8KWisCAr3mzWy2FKT6uuxQ2qGgJQxyTpDoes5': '0xsun.sol (Winrate: 83.12%, Tokens Traded: > 70)',
    '6obeVmM9SZUagyHTE7Soi7FhdZtd73m4MwHpkcL9Mu9Y': 'memescope.sol (Winrate: 34.22%, Tokens Traded: > 220)',
    '2WfNxFN74pzJWKnXQ7NpkbnbEEhSLVJZGiB9NvxQ4Vpb': 'gonzo3500.sol (Winrate: 31.05%, Tokens Traded: > 910)',
    'ArXAjxBcy18m4cZrXQaJ9E9cFdWfvGQxarHjug51V1uW': 'ArXA…V1uW (Winrate: 25.00%, Tokens Traded: > 60)',
    'HyNiuntjo51d5paTG7rX5XLLAAi68GQMN1STwSmvna4F': 'HyNi…na4F (Winrate: 62.50%, Tokens Traded: > 20)',
    }

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
MIN_BUY_AMOUNT_USD = 1000
MIN_SELL_AMOUNT_USD = 2000
RECENT_N_DAYS_INTEREST = 7
