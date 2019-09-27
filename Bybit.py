import requests
import hmac
import hashlib
import time
import json


def make_subscriptable(response):
    return json.loads(response.text)


def timestamp():
    return int(round(time.time() * 1000))  # in milliseconds


class BybitAPI:
    def __init__(self, api_key, api_secret, net):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = net

    def public_request(self, method, endpoint, params=None):
        url = self.base_url + endpoint
        if params is None:
            response = requests.request(method, url)
        else:
            response = requests.request(method, url, params=params)

        return response

    def private_request(self, method, endpoint, params=None):
        def param_construction(params, add_sign=False):

            params["api_key"] = self.api_key
            params["timestamp"] = timestamp()

            constructed_params = ""
            for key, value in sorted(params.items()):
                constructed_params = constructed_params + key + "=" + str(value) + "&"
            if constructed_params[-1] == "&":
                constructed_params = constructed_params[:-1]

            if add_sign is False:
                return bytes(constructed_params, "utf-8")
            else:
                return constructed_params + "&sign=" + signature

        def sign():
            constructed_params = param_construction(params)

            api_secret = bytes(self.api_secret, "utf-8")
            hash = hmac.new(api_secret, constructed_params, hashlib.sha256)
            return hash.hexdigest()

        if params is None:
            params = {}

        url = self.base_url + endpoint

        signature = sign()

        if method == "GET":
            params = param_construction(params, True)
            response = requests.request(method, url, params=params)
            return response
        elif method == "POST":
            params["sign"] = signature
            response = requests.request(method, url, json=params)
            return response

    def create_active_order(self, side, symbol, order_type, qty, price, time_in_force, **kwargs):
        """

        :param side:
        :param symbol:
        :param order_type:
        :param qty:
        :param price:
        :param time_in_force:
        :param take_profit: (optional)
        :param stop_loss: (optional)
        :param reduce_only: (optional)
        :param close_on_trigger: (optional)
        :param order_link_id) (optional)
        :return:
        """
        params = {
            "side": side,
            "symbol": symbol,
            "order_type": order_type,
            "qty": qty,
            "price": price,
            "time_in_force": time_in_force
        }
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("POST", "/open-api/order/create", params))

    def get_active_order(self, **kwargs):
        """

        :param order_id: (optional)
        :param order_link_id: (optional)
        :param symbol: (optional)
        :param order: (optional)
        :param page: (optional)
        :param limit: (optional)
        :param order_status: (optional)
        :return:
        """
        params = {
        }
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("GET", "/open-api/order/list", params))

    def cancel_active_order(self, order_id, **kwargs):
        """

        :param order_id:
        :param symbol: (optional)
        :return:
        """
        params = {
            "order_id": order_id
        }
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("POST", "/open-api/order/cancel", params))

    def create_cond_order(self, side, symbol, order_type, qty, price, base_price, stop_px, time_in_force, **kwargs):
        """

        :param side:
        :param symbol:
        :param order_type:
        :param qty:
        :param price:
        :param base_price:
        :param stop_px:
        :param time_in_force:
        :param close_on_trigger: (optional)
        :param order_link_id: (optional)
        :return:
        """
        params = {
            "side": side,
            "symbol": symbol,
            "order_type": order_type,
            "qty": qty,
            "price": price,
            "base_price": base_price,
            "stop_px": stop_px,
            "time_in_force": time_in_force
        }
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("POST", "/open-api/stop-order/create", params))

    def get_cond_order(self, **kwargs):
        """

        :param stop_order_id: (optional)
        :param order_link_id: (optional)
        :param symbol: (optional)
        :param order: (optional)
        :param page: (optional)
        :param limit:  (optional)
        :return:
        """
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("GET", "/open-api/stop-order/list", params))

    def cancel_cond_order(self, stop_order_id):
        """

        :param stop_order_id:
        :return:
        """
        params = {
            "stop_order_id": stop_order_id
        }
        return make_subscriptable(self.private_request("POST", "/open-api/stop-order/cancel", params))

    def get_user_leverage(self):
        """

        :return:
        """
        params = {}
        return make_subscriptable(self.private_request("GET", "user/leverage", params))

    def change_user_leverage(self, symbol, leverage):
        """

        :param symbol:
        :param leverage:
        :return:
        """
        params = {
            "symbol": symbol,
            "leverage": leverage
        }
        return make_subscriptable(self.private_request("POST", "/user/leverage/save", params))

    def get_position_list(self):
        """

        :return:
        """
        params = {}
        return make_subscriptable(self.private_request("GET", "position/list", params))

    def change_position_margin(self, symbol, margin):
        """
        seemingly does the same thing as change_user_leverage()
        :param symbol:
        :param margin:
        :return:
        """
        params = {
            "symbol": symbol,
            "margin": margin
        }
        return make_subscriptable(self.private_request("POST", "/position/change-position-margin", params))

    def get_last_funding_rate(self, symbol):
        """

        :param symbol:
        :return:
        """
        params = {
            "symbol": symbol,
        }
        return make_subscriptable(self.private_request("GET", "/open-api/funding/prev-funding-rate", params))

    def get_last_funding_fee(self, symbol):
        """

        :param symbol:
        :return:
        """
        params = {
            "symbol": symbol
        }
        return make_subscriptable(self.private_request("GET", "/open-api/funding/prev-funding", params))

    def get_predicted_funding(self, symbol):
        """

        :param symbol:
        :return:
        """
        params = {
            "symbol": symbol
        }
        return make_subscriptable(self.private_request("GET", "/open-api/funding/predicted-funding", params))

    def get_trade_records(self, order_id):
        """

        :param order_id:
        :return:
        """
        params = {
            "order_id": order_id
        }
        return make_subscriptable(self.private_request("GET", "/v2/private/execution/list", params))

    def get_orderbook(self, symbol):
        """

        :param symbol:
        :return:
        """
        params = {
            "symbol": symbol
        }
        return make_subscriptable(self.public_request("GET", "/v2/public/orderBook/L2", params))

    def get_latest_symbol_info(self):
        """

        :return:
        """
        params = {}
        return make_subscriptable(self.public_request("GET", "/v2/public/tickers", params))

    def get_wallet_fund_records(self, **kwargs):
        """

        :param start_date: (optional)
        :param end_date: (optional)
        :param currency: (optional)
        :param wallet_fund_type: (optional)
        :param page: (optional)
        :param limit: (optional)
        :return:
        """
        params = {}
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("GET", "/open-api/wallet/fund/records", params))

    def set_trading_stop(self, symbol, **kwargs):
        """

        :param symbol:
        :param take_profit: (optional)
        :param stop_loss: (optional)
        :param trailing_stop: (optional)
        :return:
        """
        params = {
            "symbol": symbol
                  }
        for key, value in kwargs.items():
            params[key] = value
        return make_subscriptable(self.private_request("POST", "/open-api/position/trading-stop", params))


