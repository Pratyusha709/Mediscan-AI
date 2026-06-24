import numpy as np

def calculate_prices(price_per_tablet, tablets_per_strip):

    # Convert to numpy
    tablet_price = np.array(price_per_tablet)
    count = np.array(tablets_per_strip)

    # Price of one strip
    strip_price = tablet_price * count

    # Multiple strips
    strips = np.array([1, 2, 3, 4])
    total_prices = strip_price * strips

    return {
        "tablet_price": float(tablet_price),
        "tablets_per_strip": int(count),
        "strip_price": float(strip_price),
        "multi_strip_prices": total_prices.tolist()
    }