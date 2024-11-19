import os
from pycoin.symbols.btc import network
import requests

# Generate a new Bitcoin private key
key = network.keys.bip32_seed(os.urandom(64))

# Get the Bitcoin address and WIF (Wallet Import Format) private key
address = key.address()
wif = key.wif()

# Create a directory to store the key if it doesn't exist
key_dir = "keys"
os.makedirs(key_dir, exist_ok=True)

# Define file paths
address_file = os.path.join(key_dir, "address.txt")
key_file = os.path.join(key_dir, "private_key.txt")

# Write the address and private key to files
with open(address_file, "w") as addr_file:
    addr_file.write(address)

with open(key_file, "w") as pk_file:
    pk_file.write(wif)

print(f"Bitcoin address and private key saved in the '{key_dir}' directory.")
