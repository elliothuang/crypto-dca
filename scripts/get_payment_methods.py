# %%
"""Run this script to get the payment methods associated with your account.

Usage: `python get_payment_methods.py <API_KEY> <SECRET_KEY> <PASSPHRASE>`
Note: The API_KEY requires "Transfer" permissions.
"""

# %%
import sys
import json

import requests

sys.path.insert(0, '../lambda/layers/package/python/')
import coinbasepro

# %%
assert len(sys.argv) == 4, "Did you execute as `python get_payment_ids.py <API_KEY> <SECRET_KEY> <PASSPHRASE>`?"
_, API_KEY, SECRET_KEY, PASSPHRASE = sys.argv

# %%
api_url = 'https://api.pro.coinbase.com/'
auth = coinbasepro.CoinbaseProAuth(API_KEY, SECRET_KEY, PASSPHRASE)

# %%
r = requests.get(api_url + 'payment-methods', auth=auth)
r.raise_for_status()

# %%
out_path = "../temp/payment_methods.json" 
with open(out_path, "w") as out:
    json.dump(r.json(), out, indent=2)

# %%
print(f"Wrote payment methods to '{out_path}'.")

# %%
