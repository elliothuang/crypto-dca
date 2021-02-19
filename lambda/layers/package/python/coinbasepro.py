import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

class CoinbaseProAuth(AuthBase):
    """Attaches Coinbase Pro Authentication headers to the given request object."""
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        # Prepare message
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url
        if request.body is not None:
            message += request.body.decode()
        
        # Sign message
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode().rstrip('\n') 

        # Update request object
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })

        return request
