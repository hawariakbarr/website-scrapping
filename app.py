import pdfkit, os, uuid, time, crochet
from operator import itemgetter
import scrapy
import requests
import logging
from operator import itemgetter

crochet.setup()

from flask import *
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

# wkhtml = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
# config = pdfkit.configuration(wkhtmltopdf=wkhtml)

# Importing our Scraping Function from the amazon_scraping file

from scrapingweb.scrapingweb.spiders.scrap_pgrt import ReviewspiderSpider

# Creating Flask App Variable

app = Flask(__name__)

Download_PATH = 'wkhtmltopdf/bin/wkhtmltopdf.exe'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Download_FOLDER = os.path.join(APP_ROOT, Download_PATH)

output_data = []
crawl_runner = CrawlerRunner()

# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
	return render_template("index.html") # Returns index.html file in templates folder.

@app.route('/export', methods=['POST'])
def export():
    # url = request.form['URL']
    try:
        
        options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
        } 
        filename = str(uuid.uuid4()) + '.pdf'
        config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
        pdfkit.from_url("http://127.0.0.1:5000/scrape", filename, configuration=config, options=options)
        pdfDownload = open(filename, 'rb').read()
        os.remove(filename)
        return Response(
            pdfDownload,
            mimetype="application/pdf",
            headers={
                "Content-disposition": "attachment; filename=" + filename,
                "Content-type": "application/force-download"
            }
        )
    except ValueError:
        print("Oops!")


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

# @app.route('/export', methods=['POST'])
# def export():
#     font_config = FontConfiguration()
#     htmlFile = HTML(".../report.html")
#     css = CSS(string='''s
#     @font-face {
#         font-family: Gentium;
#         src: url(http://example.com/fonts/Gentium.otf);
#     }
#     h1 { font-family: Gentium }''', font_config=font_config)
#     htmlFile.write_pdf(
#     '/tmp/example.pdf', stylesheets=[css],
#     font_config=font_config)

@app.route("/scrape")
def scrape():
    scrape_with_crochet(baseURL=baseURL) # Passing that URL to our Scraping Function
    time.sleep(15) # Pause the function while the scrapy spider is running
    # listData = [1,2,3,4,5]
    newlist = sorted(output_data, key=itemgetter('seq_number'), reverse=False)
    return render_template("report.html", data = newlist) # Returns the scraped data after being running for 20 seconds.
  
@crochet.run_in_reactor
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