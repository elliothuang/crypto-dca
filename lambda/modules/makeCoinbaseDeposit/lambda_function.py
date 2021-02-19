"""AWS Lambda Function to deposit money from a bank account into Coinbase Pro.

Contributors: Elliot Huang
"""

import os
import json
import logging
from base64 import b64decode

import boto3
import requests

import coinbasepro

def decrypt_env_var(encrypted):
    """Decrypts an environment variable for AWS Lambda using AWS KMS.
    
    Params:
        encrypted (str): The value of the encrypted env var

    Returns:
        decrypted (str): The decrypted env var
     """
    decrypted = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(encrypted),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    return decrypted

# Decrypt env vars outside of lambda_handler
API_KEY = decrypt_env_var(os.environ['api_key'])
SECRET_KEY = decrypt_env_var(os.environ['secret_key'])
PASSPHRASE = decrypt_env_var(os.environ['passphrase'])

def lambda_handler(event, context):
    """Makes a deposit from a payment account to a Coinbase account.

    Params:
        event (dict): This is the AWS event that invokes this Lambda function.
            It must contain a key/value pair for 'payment_method_id' and 'amount'.
    
    Returns:
        deposit_info (dict, serializable json): Contains info about the deposit.
    """
    api_url = 'https://api.pro.coinbase.com/'
    auth = coinbasepro.CoinbaseProAuth(API_KEY, SECRET_KEY, PASSPHRASE)

    deposit_info = {
        'payment_method_id': event['payment_method_id'],
        'amount': event['amount'],
        'currency': 'USD',
    }

    try:
        r = requests.post(api_url + 'deposits/payment-method', json=deposit_info, auth=auth)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        deposit_info['result'] = 'FAILED'
        deposit_info['detail'] = f"{type(e).__name__}: {e}"
        deposit_info['message'] = r.json()['message']
        logging.exception(f"Response message: {deposit_info['message']}")
    except Exception as e:
        deposit_info['result'] = 'FAILED'
        deposit_info['detail'] = f"{type(e).__name__}: {e}"
        logging.exception('An unknown error occured')
    else:
        deposit_info['result'] = 'SUCCESS'
        deposit_info['detail'] = r.json()
        msg = (
            f"SUCCESS: {deposit_info['amount']} {deposit_info['currency']} deposit "
            f"to {deposit_info['payment_method_id']} "
            f"ready on {deposit_info['detail']['payout_at']}"
        )
        print(msg)
    finally:
        return deposit_info
