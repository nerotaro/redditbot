
import praw
import random
import requests
import json


#login details
r = praw.Reddit(
    user_agent="windows:com.testapp.",
    client_id="X_ZgU4Zo9KpGwC4qpB6HyA",
    client_secret="SyW5vlv7MQYhL2lPjyKlFZxc95Sx6A",
    username="neroredditbot",
    password="typograph"
    )

subreddit = r.subreddit("botTest1ima")
#adds quotes from quotes.txt to the quotes list
quotes = []
with open("quotes.txt", "r", encoding="utf8") as f:
    for x in f:
        quotes.append(x.replace("\n", ""))
#adds comments replied to saved in the file commentsRepliedTo.txt to the list commentsRepliedTo
commentsRepliedTo = []
with open("commentsRepliedTo.txt", "r") as f:
    for x in f:
        commentsRepliedTo.append(x.replace("\n", ""))
    print("commentsRepliedTo.txt converted to list: ", commentsRepliedTo)
while True:
    for submission in subreddit.hot(limit=5):
        for comment in submission.comments:
            if "stock " in comment.body:
                if comment.id in commentsRepliedTo:
                    pass
                else:
                    import yfinance as yf
                    
                    stock = comment.body.replace("stock", "").replace(" ", "")
                    stock_info = yf.Ticker(stock.upper()).info
                    # stock_info.keys() for other properties you can explore
                    market_price = stock_info['regularMarketPrice']
                    previous_close_price = stock_info['regularMarketPreviousClose']
                    reply = str("market price:"+str(market_price)+"\nprevious close price:"+str(previous_close_price))
                    comment.reply(reply)
                    print(comment.body)
                    commentsRepliedTo.append(comment.id)
                    with open("commentsRepliedTo.txt", "w") as f:
                        for x in commentsRepliedTo:
                            f.write(x)
                            f.write("\n")
            if "quote" in comment.body:
                if comment.id in commentsRepliedTo:
                    pass
                else:
                    comment.reply(random.choice(quotes))
                    print(comment.body)
                    commentsRepliedTo.append(comment.id)
                    with open("commentsRepliedTo.txt", "w") as f:
                        for x in commentsRepliedTo:
                            f.write(x)
                            f.write("\n")
            if "define" or "definition" in comment.body:
                if not comment.id in commentsRepliedTo:
                    print(comment.body)
                    word = comment.body.replace("define ", "").replace("definition ", "")
                    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
                    querystring = {"term":word}

                    headers = {
                        "X-RapidAPI-Key": "089048036fmshf8c0f89abd73581p161612jsnee847f65edaf",
                        "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
                        }
                    response_API = requests.request("GET", url, headers=headers, params=querystring)
                    print(response_API.status_code)
                    data = response_API.text
                    parse_json = json.loads(data)

                    info = parse_json['list'][0]['definition']
                    exampleInJson = parse_json['list'][0]['example']
                    example = exampleInJson.replace("[", "").replace("]", "")
                    definition = info.replace("[", "").replace("]", "")
                    replyDefinition = f"Definition of {word}: {definition} | Example: {example} | Definition provided by urban dictionary"
                    comment.reply(replyDefinition)
                    commentsRepliedTo.append(comment.id)
                    with open("commentsRepliedTo.txt", "w") as f:
                        for x in commentsRepliedTo:
                            f.write(x)
                            f.write("\n")

            if "weather" in comment.body:
                if not comment.id in commentsRepliedTo:
                    print(comment.body)

