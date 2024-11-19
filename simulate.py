import csv
import datetime
import time
import requests

# CoinGecko API URL for Bitcoin price in USD
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&precision=18"

# Output CSV file
CSV_FILE = "bitcoin_price_log.csv"

# Function to initialize the CSV file
def initialize_csv(file_name):
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Timestamp", "Price (USD)"])

# Function to log data to the CSV file
def log_to_csv(file_name, timestamp, price):
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, price])

# Function to fetch Bitcoin price
def fetch_bitcoin_price():
    try:
        response = requests.get(COINGECKO_API_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        # Extract the price of Bitcoin in USD
        price = data["bitcoin"]["usd"]
        return price
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

# Main function
def main():
    # Initialize CSV
    initialize_csv(CSV_FILE)
    print("Logging Bitcoin prices...")

    try:
        while True:
            # Fetch Bitcoin price
            price = fetch_bitcoin_price()

            if price is not None:
                # Get current timestamp
                timestamp = datetime.datetime.now().isoformat()

                # Log to CSV
                log_to_csv(CSV_FILE, timestamp, price)

                # Print to console
                print(f"Logged: Timestamp={timestamp}, Price=${price}")
            
            # Wait for 60 seconds before fetching again
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")

main()
