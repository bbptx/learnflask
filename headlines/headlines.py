import feedparser
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import json
#import urllib2
import urllib
import datetime

app = Flask(__name__)

RSS_FEEDS = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml", 
			 "cnn": "http://rss.cnn.com/rss/edition.rss",
			 "fox": "http://feeds.foxnews.com/foxnews/latest" }
			 
DEFAULTS = {"publication":"bbc", "city":"Roanoke, US", "currency_from":"INR", "currency_to":"USD"}

WEATHER_URL =  "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c2642ba2d65c8ad302e27ad09c5ac481"  # add &units=metric  for Celsius and &#8451 in template for 'C'
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=44d4d9c50dff46149037df707c4d494d"
			 
@app.route("/")
#@app.route("/<publication>")
#@app.route("/", methods=['GET','POST'])

def home():
	# get customized headlines, based on user input or default
	publication = get_value_with_fallback("publication")
	articles = get_news(publication)
	
	# get customized weather based on user input or default
	city = get_value_with_fallback('city')
	weather = get_weather(city)
	
	# get customized currency based on user input or default
	currency_from = get_value_with_fallback('currency_from')
	currency_to = get_value_with_fallback('currency_to')
	rate, currencies = get_rates(currency_from, currency_to)
	
	#return render_template("home.html", publication=publication, articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies))#
	
	#save cookies and return template
	response = make_response(render_template("home.html", publication=publication, articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies)))
	expires = datetime.datetime.now() + datetime.timedelta(days=365)
	response.set_cookie("publication", publication, expires=expires)
	response.set_cookie("city", city, expires=expires)
	response.set_cookie("currency_from",
		currency_from, expires=expires)
	response.set_cookie("currency_to", currency_to, expires=expires)
	return response
	
def get_value_with_fallback(key):
	if request.args.get(key):
		return request.args.get(key)
	if request.cookies.get(key):
		return request.cookies.get(key)
	return DEFAULTS[key]
	
def get_news(query):
	#query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication=DEFAULTS["publication"]
	else:
		publication = query.lower()
	
	feed = feedparser.parse(RSS_FEEDS[publication])
	#weather = get_weather("Roanoke, US")
	#return render_template("home.html", publication=publication, articles=feed['entries'], weather=weather)
	return feed['entries']

def get_rates(frm, to):
	all_currency = urllib.request.urlopen(CURRENCY_URL).read()
	parsed = json.loads(all_currency).get("rates")
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate/frm_rate, parsed.keys())

	
def get_weather(query):
	api_url = WEATHER_URL
	query = urllib.parse.quote(query)
	url = api_url.format(query)
	data = urllib.request.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	
	if parsed.get("weather"):
		weather = {"description": parsed["weather"][0]["description"], 
			"temperature": parsed["main"]["temp"],
			"city":parsed["name"],
			"country":parsed["sys"]["country"]
			}
	return weather

	
"""
def get_news(publication="bbc"):
	feed = feedparser.parse(RSS_FEEDS[publication])
	first_article = feed['entries'][0]
	
	return render_template("home.html", publication=publication, articles=feed['entries'])
	
	""""""
	return render_template("home.html", publication=publication, article=first_article)
	
	
	return render_template("home.html",publication=publication, title=first_article.get("title"),
		published=first_article.get("published"), 
		summary=first_article.get("summary"))
	
	
	return <html>
		<body>
			<h1> Headlines from {0} </h1>
			<b>{1}</b> <br/>
			<i>{2}</i> <br/>
			<p>{3}</p> <br/>
		</body>
	</html>.format(publication, first_article.get("title"), first_article.get("published"), first_article.get("summary")   )
	"""""" 

"""
	

if __name__ == "__main__":
	app.run(port=5000, debug=True)

