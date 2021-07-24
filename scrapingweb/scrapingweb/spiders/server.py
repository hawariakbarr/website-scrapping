# server.py
import json, subprocess, uuid, subprocess
from operator import itemgetter

from flask import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('/templates/index.html')

@app.route('/scrape')
def hello_world():
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl dmoz -o "output.json"

    wait for  this command to finish, and read output.json to client.
    """
    spider_name = "pgrt"
    # os.chdir(scapy_path)
    # D:\hawari\side project\Scraping\website scraping\scrapingweb\scrapingweb\spiders
    # call(["scrapy", "crawl", "{0}".format(spider_name), "-o output.json"])
    subprocess.check_output(['scrapy', 'crawl', spider_name, '-o', "output.json"])
    with open("output.json") as items_file:
        res = json.loads(items_file.read())
        newlist = sorted(res, key=itemgetter('seq_number'), reverse=False)
        return render_template('report.html', data=newlist)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
# server.py
    
