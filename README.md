# crypto-dca
![system_architecture_diagram](/docs/system_architecture.png)

## Purpose
When trading cryptocurrency for speculative purposes it is generally advised to buy low and sell high. However, due to the extreme volatility of cryptocurrency prices, it is often impossible to time the market profitably in this way. The strategy implemented by this system is simple [dollar cost averaging](https://en.wikipedia.org/wiki/Dollar_cost_averaging). The intent is to buy small amounts of cryptocurrency on a fixed interval (every 1 day or less) over a somewhat longer period of time (1 or more years). This system is a low-cost method to automate small dollar value cryptocurrency purchases.

## High Level System Description
There are two independent AWS Lambda functions currently implemented and they both operate in the same general way. The Lambda functions are triggered by an EventBridge rule that provides a JSON input to the Lambda function. When the Lambda function is triggered, the function decrypts stored encrypted API credentials, takes the input from the EventBridge JSON input, and makes the appropriate API call to the Coinbase Pro API. When the Lambda function receives the response from the Coinbase Pro API, it returns information about the response to Simple Notification Service (SNS) which is in turn sends an e-mail notification to the system owner.

## Future Enhancement
There could still be significant price volatility even over relatively short buy intervals. Instead of buying at the same time over a fixed interval, an enhancement of the system could be to buy when the price appears to be at a minimum over the interval. For example, consider a system that buys exactly once per day at exactly 00:00. An enhancement could be to allow to the system to buy once at any time between 00:00 - 23:59 if the model predicts that the price at that time will be the lowest in that 24-hour period. Example inputs to this model could be standard technical indicators based on trading price and volume but could also include things like social media sentiment.
