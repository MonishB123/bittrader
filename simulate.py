import requests
from datetime import datetime, timedelta  

class TradingSim():
    def __init__(self):
        pass
    def fetch_bitcoin_prices(self, start_date, end_date, interval):
        """
        Fetch Bitcoin prices between two dates at a specified interval.

        :param start_date: Start date in 'YYYY-MM-DD' format.
        :param end_date: End date in 'YYYY-MM-DD' format.
        :param interval: Interval ('daily', 'hourly').
        :return: List of prices at the specified interval.
        """
        # Convert dates to Unix timestamps
        start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

        # Validate interval
        if interval not in ["daily", "hourly"]:
            raise ValueError("Interval must be 'daily' or 'hourly'.")

        # Determine granularity
        granularity = "minutely" if interval == "hourly" else "daily"
        url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
        
        # Fetch data
        response = requests.get(
            url,
            params={
                "vs_currency": "usd",
                "from": start_timestamp,
                "to": end_timestamp,
            },
        )

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.json()}")

        data = response.json()
        prices = []

        # Extract prices
        for price_data in data["prices"]:
            timestamp, price = price_data
            dt = datetime.fromtimestamp(timestamp / 1000)  # Convert ms to s
            if interval == "hourly":
                if dt.minute == 0:  # Capture hourly prices only
                    prices.append({"date": dt, "price": price})
            else:  # Daily interval
                prices.append({"date": dt.date(), "price": price})

        return prices
