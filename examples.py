from python_bybit_API_implementation.Bybit import BybitAPI
from python_bybit import useful_funcs

# create the client using an API key and secret which can be generated on the Bybit website:
# https://www.bybit.com/app/user/api-management
api_key = ""     # API Key
api_secret = ""  # Private Key
client = BybitAPI(api_key, api_secret, "https://api.bybit.com/")  # the URL indicates mainnet or testnet


# all responses are returned as dicts
# find example responses for all endpoints here:
# https://github.com/bybit-exchange/bybit-official-api-docs/blob/master/en/rest_api.md

# creating a market buy order for market BTCUSD
response = client.create_active_order(symbol="BTCUSD",
                                      order_type="Market",
                                      side="Buy",
                                      qty=10,
                                      price="",
                                      time_in_force="GoodTillCancel")

# get the order's order ID
order_id = response["result"]["order_id"]

# print the response
useful_funcs.prettyprint(response)


# adjust leverage to 5x for market ETHUSD
client.change_user_leverage("ETHUSD", 5)
