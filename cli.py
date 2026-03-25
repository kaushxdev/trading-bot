import argparse
import os
import sys
from dotenv import load_dotenv
from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate

load_dotenv()
setup_logging()
logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="place orders on binance futures testnet")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], dest="order_type")
    parser.add_argument("--qty", required=True, type=float)
    parser.add_argument("--price", type=float, default=None, help="required for LIMIT")

    args = parser.parse_args()

    errors = validate(args.symbol, args.side, args.order_type, args.qty, args.price)
    if errors:
        print("\nvalidation failed:")
        for e in errors:
            print(f"  - {e}")
        print()
        sys.exit(1)

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("missing API keys, make sure .env is set up")
        sys.exit(1)

    print(f"\nplacing {args.order_type} {args.side} order...")
    print(f"  symbol: {args.symbol.upper()}")
    print(f"  qty: {args.qty}")
    if args.order_type == "LIMIT":
        print(f"  price: {args.price}")
    print()

    try:
        client = BinanceClient(api_key, api_secret)
        result = place_order(client, args.symbol, args.side, args.order_type, args.qty, args.price)

        print("order placed!")
        print(f"  order id  : {result.get('orderId')}")
        print(f"  status    : {result.get('status')}")
        print(f"  filled qty: {result.get('executedQty')}")
        print(f"  avg price : {result.get('avgPrice', 'N/A')}")
        print()

    except (ConnectionError, TimeoutError) as e:
        print(f"network error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error("order failed: %s", e)
        print(f"something went wrong: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()