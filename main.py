import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME="Tesla Inc"

STOCK_ENDPOINT="https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_API_KEY="TSDLNPGPPXVVOMZH"
NEWS_API_KEY ="e086890aa0f944c8bb8ad9b96befa72c"
TWILIO_SID = "AC1f7918ae25a4ac23d7d875b1a1d5c916"
TWILIO_AUTH_TOKEN = "785e4215602133c0f1bab337ccbacf88"

stock_params={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
# GET yesterday closing price
response = requests.get(STOCK_ENDPOINT,params = stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

# Get day before yesterday closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

# Find the positive difference
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

# Calculate diff_percent
diff_percent = (difference/float(yesterday_closing_price)) * 100
print(diff_percent)

# If diff_percent is greater than 2.5, then Get News
if diff_percent > 0.01 :
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,

    }
    news_response = requests.get(NEWS_ENDPOINT, params = news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client= Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18623226931",
            to ="+918077875725",
        )