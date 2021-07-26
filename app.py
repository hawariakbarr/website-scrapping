import os, crochet, time, requests, weasyprint
from jinja2 import Environment, FileSystemLoader
from subprocess import call
from bs4 import BeautifulSoup
from pathlib import Path
from operator import itemgetter
from flask import *
from scrapy.crawler import CrawlerRunner
# Importing our Scraping Function from the amazon_scraping file
from scrapingweb.scrapingweb.spiders.scrap_pgrt import ReviewspiderSpider

crochet.setup()     # initialize crochet

# Creating Flask App Variable
app = Flask(__name__)

crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
quotes_list = []                    # store quotes
scrape_in_progress = False
scrape_complete = False

ROOT = r'D:\hawari\side project\Scraping\website scraping'
ASSETS_DIR = os.path.join(ROOT, 'assets')

TEMPLAT_SRC = os.path.join(ROOT, 'templates')
CSS_SRC = os.path.join(ROOT, 'static/css')
DEST_DIR = os.path.join(ROOT, 'output')

TEMPLATE = 'report.html'
CSS = 'style.css'
OUTPUT_FILENAME = 'my-report.pdf'

@app.route('/forceresult')
def force_result():
    with open('outputdata.json') as items_file:
        res = json.loads(items_file.read())
    return render_template('report.html', data=res)

# @app.route('/export')
# def print_pdf():
#     print('start generate report...')
    # env = Environment(loader=FileSystemLoader(TEMPLAT_SRC))
    # template = env.get_template(TEMPLATE)
    # css = os.path.join(CSS_SRC, CSS)

    # # variables
    # template_vars = { 'assets_dir': 'file://' + ASSETS_DIR }

    # # rendering to html string
    # rendered_string = template.render(template_vars)
    # report = os.path.join(DEST_DIR, OUTPUT_FILENAME)
    # html.write_pdf(report, stylesheets=[css])
    # headers = {
    #     'Access-Control-Allow-Origin': '*',
    #     'Access-Control-Allow-Methods': 'GET',
    #     'Access-Control-Allow-Headers': 'Content-Type',
    #     'Access-Control-Max-Age': '3600',
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    # }
    # url = "http://127.0.0.1:5000/results"
    # req = requests.get(url)
    # time.sleep(3) #if you want to wait 3 seconds for the page to load
    # soup = BeautifulSoup(req.text, 'html.parser')
    # page = soup.find("div", {"id": "dvContainer"})
    # print(soup.prettify())
    # print(page.prettify())
    # html = weasyprint.HTML(string=str(page))
    # html.write_pdf(report, stylesheets=[css])
    # print('file is generated successfully and under')
    # return redirect(url_for('index'))

# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
	return render_template("index.html") # Returns index.html file in templates folder.
    # return 'Welcome to the jungle'

@app.route('/greeting')
@app.route('/greeting/<name>')
def greeting(name='World'):
    return 'Hello %s!' % (name)

@app.route('/crawl', methods=['GET', 'POST'])
def crawl_for_quotes():
    """
    Scrape for quotes
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global quotes_list
        # start the crawler and execute a callback when complete
        scrape_with_crochet(quotes_list)
        return render_template('loading.html')
    elif scrape_complete:
        if os.path.exists("outputdata.json"): 
        	os.remove("outputdata.json")
        newlist = sorted(quotes_list, key=itemgetter('seq_number'), reverse=False)
        with open('outputdata.json', 'w') as f:
            json.dump(newlist, f, indent=4)
         # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
        return redirect(url_for('get_results'))        
        # return "Scraping Complete"
    time.sleep(3)
    return render_template('loading.html')
    # return "Scraping Still In Progress"

@app.route('/results', methods=['GET', 'POST'])
def get_results():
    """
    Get the results only if a spider has results
    """
    # global scrape_complete
    # if scrape_complete:
    time.sleep(3)
    with open('outputdata.json') as items_file:
        res = json.loads(items_file.read())
    return render_template("report.html", data = res) # Returns the scraped data
    # return redirect(url_for('crawl_for_quotes'))

@app.route('/home')
def go_home():
    crawl_runner.stop()
    global scrape_in_progress
    global scrape_complete
    global quotes_list
    quotes_list = []
    scrape_in_progress = False
    scrape_complete = False
    return render_template("index.html")

@crochet.run_in_reactor
def scrape_with_crochet(_list):
    eventual = crawl_runner.crawl(ReviewspiderSpider, quotes_list =_list)
    eventual.addCallback(finished_scrape)

def finished_scrape(null):
    """
    """
    global scrape_complete
    scrape_complete = True

    
if __name__== "__main__":
    app.run(debug=True)
# if __name__== "__main__":
#     app.run(debug=True)
# After clicking the Submit Button FLASK will come into this
# @app.route('/', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         s = request.form['url'] # Getting the Input Amazon Product URL
#         global baseURL
#         baseURL = s
        
#         # This will remove any existing file with the same name so that the scrapy will not append the data to any previous file.
#         if os.path.exists("/scrapingnweb/outputfile.json"): 
#         	os.remove("/scrapingnweb/outputfile.json")

#         return redirect(url_for('scrape')) # Passing to the Scrape function
#         # return "Scrapping finished"

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

# @app.route("/scrape")
# def scrape():
#     scrape_with_crochet(baseURL=baseURL) # Passing that URL to our Scraping Function
#     time.sleep(15) # Pause the function while the scrapy spider is running
#     # listData = [1,2,3,4,5]
#     newlist = sorted(output_data, key=itemgetter('seq_number'), reverse=False)
#     return json.dumps(newlist)
  
# @crochet.run_in_reactor
# def scrape_with_crochet(baseURL):
#     # This will connect to the dispatcher that will kind of loop the code between these two functions.
#     dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
#     # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
#     eventual = crawl_runner.crawl(ReviewspiderSpider, category = baseURL)
#     eventual.addCallback(finished_scrape)

# def finished_scrape(null):
#     """
#     A callback that is fired after the scrape has completed.
#     Set a flag to allow display the results from /results
#     """
#     global scrape_complete
#     scrape_complete = True

# #This will append the data to the output data list.
# def _crawler_result(item, response, spider):
#     output_data.append(dict(item))

# @app.route('/export', methods=['POST'])
# def export():
#     # url = request.form['URL']
#     try:
#         options = {
#         'page-size': 'Letter',
#         'margin-top': '0.75in',
#         'margin-right': '0.75in',
#         'margin-bottom': '0.75in',
#         'margin-left': '0.75in',
#         'encoding': "UTF-8",
#         'no-outline': None
#         } 
#         filename = str(uuid.uuid4()) + '.pdf'
#         config = pdfkit.configuration(wkhtmltopdf=Download_FOLDER)
#         pdfkit.from_url("http://127.0.0.1:5000/scrape", filename, configuration=config, options=options)
#         pdfDownload = open(filename, 'rb').read()
#         os.remove(filename)
#         return Response(
#             pdfDownload,
#             mimetype="application/pdf",
#             headers={
#                 "Content-disposition": "attachment; filename=" + filename,
#                 "Content-type": "application/force-download"
#             }
#         )
#     except ValueError:
#         print("Oops!")
