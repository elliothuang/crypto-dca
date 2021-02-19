"""AWS Lambda Function to place an order on Coinbase Pro.

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
    """Places a Coinbase order.

    Params:
        event (dict): This is the AWS event that invokes this Lambda function.
            It must contain a key 'order_params' that contains the correct
            parameters for the order. This function does NOT check to ensure
            the parameters are correct.
    
    Returns:
        order_info (dict, serializable json): Contains info about the order.
    """
    api_url = 'https://api.pro.coinbase.com/'
    auth = coinbasepro.CoinbaseProAuth(API_KEY, SECRET_KEY, PASSPHRASE)

    order_params = event['order_params']
    order_info = {}

    try:
        r = requests.post(api_url + 'orders', json=order_params, auth=auth)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        order_info['result'] = 'FAILED'
        order_info['detail'] = f"{type(e).__name__}: {e}"
        order_info['message'] = r.json()['message']
        logging.exception(f"Response message: {order_info['message']}")
    except Exception as e:
        order_info['result'] = 'FAILED'
        order_info['detail'] = f"{type(e).__name__}: {e}"
        logging.exception('An unknown error occured')
    else:
        order_info['result'] = 'PLACED'
        order_info['detail'] = r.json()
        msg = (
            f"ORDER PLACED: '{order_info['detail']['id']}' "
            f"{order_info['detail']['type']} "
            f"{order_info['detail']['side']} "
            f"{order_info['detail']['product_id']} "
            f"@ {order_info['detail']['funds']} fiat "
            f"on {order_info['detail']['created_at']}"
        )
        print(msg)
    finally:
        return order_info
