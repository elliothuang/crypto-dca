#!/bin/bash
set -eo pipefail

# Temp move away
COINBASEPROPY="./package/python/coinbasepro.py"
[ -f "$COINBASEPROPY" ] && mv "$COINBASEPROPY" ./

# Fresh install of packages
rm -rf package
pip install --target ./package/python -r requirements.txt

# Move back
mv ./coinbasepro.py package/python

# Create zip for manual upload to AWS Lambda
cd package
zip -r ../crypto-dca-lib.zip python
