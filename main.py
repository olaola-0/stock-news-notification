"""
This module fetches the stock price of a particular company from the Alpha Vantage API.
If the stock price changes more than 0.65%, it fetches the top 3 news related to the company from the News API.
It then sends a brief about these news articles through SMS using Twilio API.
"""
import os
import requests
from twilio.rest import Client

# The API endpoint for fetching stock data from Alpha Vantage.
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

# The stock symbol of the company for which the data is to be fetched.
STOCK = "TSLA"

# The API Key for Alpha Vantage.
ALPHA_VANTAGE_STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_STOCK_API_KEY")

# Parameters for the GET request to Alpha Vantage.
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_STOCK_API_KEY,
}

# The API endpoint for fetching news data from News API.
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# The name of the company for which the news is to be fetched.
COMPANY_NAME = "Tesla Inc"

# The API Key for News API.
NEWS_ORG_API_KEY = os.getenv("NEWS_ORG_API_KEY")

# Parameters for the GET request to News API.
news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_ORG_API_KEY,
    "language": "en",
}

# Twilio Account SID, Auth Token, and phone numbers for sending SMS.
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
RECIPIENT_NUMBER = os.getenv("RECIPIENT_NUMBER")

# Fetch the stock data.
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

# Extract and compute the necessary data.
data_list = [value for (key, value) in data.items()]
previous_day_data = data_list[0]
previous_day_opening_price = float(previous_day_data["1. open"])
previous_day_closing_price = float(previous_day_data["4. close"])
day_before_previous_day_data = data_list[1]
day_before_opening_price = float(day_before_previous_day_data["1. open"])
day_before_closing_price = float(day_before_previous_day_data["4. close"])
difference = previous_day_closing_price - day_before_closing_price
up_and_down = "🔺" if difference > 0 else "🔻"
difference_percentage = (difference / previous_day_closing_price) * 100
rounded_difference_percentage = round(difference_percentage, 2)


def get_news():
    """
    This function fetches the top 3 news articles related to the company if the stock price change
    is more than 0.65%.
    """
    if abs(rounded_difference_percentage) > 0.65:
        news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
        news_response.raise_for_status()
        news_articles = news_response.json()["articles"]
        news = [f"{STOCK}: {up_and_down}{rounded_difference_percentage}%\n"]
        for i in range(3):
            news_source_name = news_articles[i]["source"]["name"]
            headline = news_articles[i]["title"]
            brief = news_articles[i]["description"]
            news_url = news_articles[i]["url"]
            news.append(
                f"News Source: {i + 1}. {news_source_name}\n"
                f"Headline: {i + 1} {headline}\n"
                f"Brief: {brief}\n"
                f"News URL: {news_url}.\n"
            )
        return "\n".join(news)


# Get the news and send it as an SMS.
news_text = get_news()
if news_text:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=news_text,
        from_=TWILIO_NUMBER,
        to=RECIPIENT_NUMBER
    )
    # print(message.sid)
