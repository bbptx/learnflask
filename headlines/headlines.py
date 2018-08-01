import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {"bbc": "http://feeds.bbci.co.uk/news/rss.xml", 
			 "cnn": "http://rss.cnn.com/rss/edition.rss",
			 "fox": "http://feeds.foxnews.com/foxnews/latest" }
			 
@app.route("/")
#@app.route("/<publication>")

def get_news():
	query = request.args.get("publication")
	if not query or query.lower() not in RSS_FEEDS:
		publication="bbc"
	else:
		publication = query.lower()
	
	feed = feedparser.parse(RSS_FEEDS[publication])
	
	return render_template("home.html", publication=publication, articles=feed['entries'])

	
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

