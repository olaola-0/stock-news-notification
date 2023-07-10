# Stock News Notification
This project fetches the stock price of a particular company from the Alpha Vantage API. If the stock price changes by more than 0.65%, it fetches the top 3 news related to the company from the News API. It then sends a brief about these news articles through SMS using Twilio API.

## Features
* Fetches stock data from Alpha Vantage API.
* Calculates the percentage difference in closing prices between two days.
* If the stock price changes by more than 0.65%, fetches the top 3 news articles related to the company from the News API.
* Sends an SMS with the percentage change and a brief about the news articles.


## Getting Started
### Prerequisites
* Python 3
* A Twilio account for sending SMS
* Alpha Vantage API for fetching stock data
* NEWS API key for fetching news data


## Installation
1. Clone the repo:
```
git clone https://github.com/olaola-0/stock-news-notification.git
```
2. Install the required Python packages:
```
pip install -r requirements.txt
```
3. Set up the following environment variables:
```
ALPHA_VANTAGE_STOCK_API_KEY = "Your Alpha Vantage API Key"
NEWS_ORG_API_KEY = "Your News API Key"
TWILIO_ACCOUNT_SID = "Your Twilio Account SID"
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token"
TWILIO_NUMBER = "Your Twilio Phone Number"
RECIPIENT_NUMBER = "Recipient's Phone Number"
```
4. Run main.py:
```
python main.py
```

## Usage
The script will automatically fetch the stock price for the company specified in the STOCK variable and send an SMS if the price changes by more than 0.65%. You can modify the STOCK and COMPANY_NAME variables to get data for different companies.


## API Documentation
* [Alpha Vantage API](https://www.alphavantage.co/documentation/)
* [News API](https://newsapi.org/docs)
* [Twilio API](https://www.twilio.com/docs/quickstart/python/sms#overview)


## Acknowledgments
* Twilio for their simple-to-use API for sending SMS
* Alpha Vantage and News API for their extensive and easy to use APIs
