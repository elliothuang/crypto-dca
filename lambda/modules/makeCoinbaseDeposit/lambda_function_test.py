# %%
import os
import json
import time

sys.path.insert(0, '../../layers/package/python/')
import coinbasepro

#%%
# Set env vars
os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'makeCoinbaseDeposit'

fp = '../../../temp/crypto-dca-full-aws_encrypted_d.json'
with open(fp, 'r') as f:
    api_info = json.load(f)

os.environ['api_key'] = api_info['api_key']
os.environ['secret_key'] = api_info['secret_key']
os.environ['passphrase'] = api_info['passphrase']

# %%
import lambda_function

# %%
# Set test event and context
fp = '../../../temp/deposit_payment_methods.json'
with open(fp, 'r') as f:
    payment_methods = json.load(f)

event = {
    'payment_method_id': payment_methods['personal_checking_account'],
    'amount': '10.00'
}

context = None

# %%
start = time.time()
r = lambda_function.lambda_handler(event, context)
end = time.time()
print(f"Execution time: {end - start} sec")

# %%
r

# %%
