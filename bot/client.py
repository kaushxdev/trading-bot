import hashlib
import hmac
import time
import requests
from bot.logging_config import get_logger

logger = get_logger(__name__)

BASE_URL = "https://demo-fapi.binance.com"


class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params):
        query = "&".join(f"{k}={v}" for k, v in params.items())
        sig = hmac.new(
            self.api_secret.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = sig
        return params

    def post(self, endpoint, params):
        params["timestamp"] = int(time.time() * 1000)
        params = self._sign(params)
        url = BASE_URL + endpoint

        logger.info("request -> %s params: %s", endpoint, {k: v for k, v in params.items() if k != "signature"})

        try:
            res = self.session.post(url, params=params, timeout=10)
            data = res.json()
            logger.info("response -> %s", data)

            if not res.ok:
                raise requests.HTTPError(f"API error {data.get('code')}: {data.get('msg')}")

            return data

        except requests.exceptions.ConnectionError:
            logger.error("couldnt reach testnet, check internet")
            raise ConnectionError("Couldnt connect to Binance testnet")

        except requests.exceptions.Timeout:
            logger.error("request timed out")
            raise TimeoutError("Request timed out")