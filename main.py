import crochet
from operator import itemgetter
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

crochet.setup()

from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import time
import os

# Importing our Scraping Function from the amazon_scraping file

from scrapingweb.scrapingweb.spiders.scrap_pgrt import ReviewspiderSpider

# Creating Flask App Variable

app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
	return render_template("index.html") # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        s = request.form['url'] # Getting the Input Amazon Product URL
        global baseURL
        baseURL = s
        
        # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
        if os.path.exists("/scrapingnweb/outputfile.json"): 
        	os.remove("/scrapingnweb/outputfile.json")

        return redirect(url_for('scrape')) # Passing to the Scrape function

@app.route('/export', methods=['POST'])
def export():
    font_config = FontConfiguration()
    htmlFile = HTML(".../report.html")
    css = CSS(string='''
    @font-face {
        font-family: Gentium;
        src: url(http://example.com/fonts/Gentium.otf);
    }
    h1 { font-family: Gentium }''', font_config=font_config)
    htmlFile.write_pdf(
    '/tmp/example.pdf', stylesheets=[css],
    font_config=font_config)

@app.route("/scrape")
def scrape():
    scrape_with_crochet(baseURL=baseURL) # Passing that URL to our Scraping Function
    time.sleep(20) # Pause the function while the scrapy spider is running
    # listData = [1,2,3,4,5]
    newlist = sorted(output_data, key=itemgetter('seq_number'), reverse=False)
    return render_template("report.html", data = newlist) # Returns the scraped data after being running for 20 seconds.
  
@crochet.run_in_reactor
@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(baseURL):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
    eventual = crawl_runner.crawl(ReviewspiderSpider, category = baseURL)
    eventual.addCallback(finished_scrape)

def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    output_data.append(dict(item))


if __name__== "__main__":
    app.run(debug=True)