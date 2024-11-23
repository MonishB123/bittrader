import csv
import requests
import time
from datetime import datetime

# Binance API endpoints
BASE_URL = "https://api.binance.us/api/v3/"
TICKER_PRICE_URL = f"{BASE_URL}ticker/price"
AVERAGE_PRICE_URL = f"{BASE_URL}avgPrice"
ORDER_BOOK_PRICE_URL = f"{BASE_URL}ticker/bookTicker"

# Trading symbol (e.g., BTCUSD)
SYMBOL = "BTCUSDT"

# Fetch Live Ticker Price
def fetch_ticker_price(symbol):
    try:
        response = requests.get(TICKER_PRICE_URL, params={"symbol": symbol})
        response.raise_for_status()
        return response.json().get("price")
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching ticker price: {e}")
        return None

# Fetch Average Price
def fetch_average_price(symbol):
    try:
        response = requests.get(AVERAGE_PRICE_URL, params={"symbol": symbol})
        response.raise_for_status()
        return response.json().get("price")
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching average price: {e}")
        return None

# Fetch Best Order Book Prices
def fetch_order_book_price(symbol):
    try:
        response = requests.get(ORDER_BOOK_PRICE_URL, params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()
        return data.get("bidPrice"), data.get("askPrice")
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching order book prices: {e}")
        return None, None

# Write data into a CSV file
def write_to_csv(file_name, ticker_price, avg_price, bid_price, ask_price):
    try:
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Add a header row if the file is empty
            if file.tell() == 0:
                writer.writerow(["Timestamp", "Ticker Price", "Average Price", "Bid Price", "Ask Price"])
            # Write the data
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ticker_price,
                avg_price,
                bid_price,
                ask_price
            ])
    except Exception as e:
        log_error(f"Error writing to CSV: {e}")

# Log errors into a log file
def log_error(message):
    with open("error_log.txt", mode='a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Main function
def main():
    file_name = "binance_prices.csv"
    while True:
        try:
            # Fetch data
            ticker_price = fetch_ticker_price(SYMBOL)
            avg_price = fetch_average_price(SYMBOL)
            bid_price, ask_price = fetch_order_book_price(SYMBOL)

            # Check if data is valid before writing to the CSV
            if ticker_price and avg_price and bid_price and ask_price:
                write_to_csv(file_name, ticker_price, avg_price, bid_price, ask_price)
                print(f"Data written: Ticker: {ticker_price}, Avg: {avg_price}, Bid: {bid_price}, Ask: {ask_price}")
            else:
                log_error("Incomplete data fetched. Skipping CSV write.")

            # Sleep to avoid rate limits
            time.sleep(1)

        except Exception as e:
            log_error(f"Unexpected error in main loop: {e}")
            time.sleep(5)  # Back off if an unexpected error occurs

# Run the script
if __name__ == "__main__":
    main()
