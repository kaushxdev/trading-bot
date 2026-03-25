from bot.logging_config import get_logger

logger = get_logger(__name__)


def place_order(client, symbol, side, order_type, qty, price=None):
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": qty,
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info("placing order: %s", params)
    return client.post("/fapi/v1/order", params)