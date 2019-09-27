# python-Bybit-API-implementation

Find Bybit cryptocurrency exchange here: https://www.bybit.com/

Find the official API docs here: https://github.com/bybit-exchange/bybit-official-api-docs

This is a temporary wrapper as Bybit is working on implementing with CCXT.

This wrapper does not have websocket support, only access to the rest API endpoints (for both public and private topics).

Again, this is temporary - I will not be adding any features although I may merge pull requests.

## Usage
Find examples in the `examples.py` file. Here is an extract:
```py
api_key = ""     # API Key
api_secret = ""  # Private Key
client = BybitAPI(api_key, api_secret, "https://api.bybit.com/")  # the URL indicates mainnet or testnet

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
```
