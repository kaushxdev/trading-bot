VALID_SIDES = ["BUY", "SELL"]
VALID_TYPES = ["MARKET", "LIMIT"]


def validate(symbol, side, order_type, qty, price):
    errors = []

    if not symbol or not symbol.strip():
        errors.append("symbol cant be empty")

    if side.upper() not in VALID_SIDES:
        errors.append(f"side should be BUY or SELL, got '{side}'")

    if order_type.upper() not in VALID_TYPES:
        errors.append(f"order type should be MARKET or LIMIT, got '{order_type}'")

    if qty <= 0:
        errors.append("qty has to be greater than 0")

    if order_type.upper() == "LIMIT":
        if price is None:
            errors.append("price is required for limit orders")
        elif price <= 0:
            errors.append("price has to be greater than 0")

    return errors