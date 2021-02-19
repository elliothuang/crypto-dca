# %%
import os
import json
import time

sys.path.insert(0, '../../layers/package/python/')
import coinbasepro

#%%
# Set env vars
os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'placeCoinbaseOrder'

fp = '../../../temp/crypto-dca-full-aws_encrypted_o.json'

with open(fp, 'r') as f:
    api_info = json.load(f)

os.environ['api_key'] = api_info['api_key']
os.environ['secret_key'] = api_info['secret_key']
os.environ['passphrase'] = api_info['passphrase']

# %%
import lambda_function

# %%
# Set test event and context
event = {
    'order_params': {
        'side': 'buy',
        'product_id': 'BTC-USD',
        'type': 'market',
        'funds': '20'
    },

    'other_key': 'val',
    'another_key': 'val2',
    'yet_another_key': [
        'list',
        'of',
        'vals'
    ]
}
context = None

# %%
start = time.time()
order_info = lambda_function.lambda_handler(event, context)
end = time.time()
print(f"Execution time: {end - start} sec")

# %%
order_info

# %%
