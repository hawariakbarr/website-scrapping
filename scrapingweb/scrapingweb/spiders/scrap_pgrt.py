import scrapy
import requests
import logging
from operator import itemgetter

class MyItem(scrapy.Item):
    images = scrapy.Field()
    nextPage = scrapy.Field(default = 'null')

class ReviewspiderSpider(scrapy.Spider):
    name = 'pgrt'
    # start_urls=["https://125.213.129.105/controls/objectgraph.htm?id=0&graphid=2&columns=datetime,value_,coverage&_=1625796838093&Username=Diskominfo%20Jabar&Password=P4sswordJabar"]
    #     # "https://125.213.129.105/controls/objectgraph.htm?id=0&graphid=3&columns=datetime,value_,coverage&_=1625796838093&Username=Diskominfo%20Jabar&Password=P4sswordJabar",
    # ]

    myBaseUrl = ''
    start_urls = []
    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    custom_settings = {'FEED_URI': 'scrapingweb/outputfile.json', 'CLOSESPIDER_TIMEOUT' : 20} # This will tell scrapy to store the scraped data to outputfile.json and for how long the spider should run.

    def parse(self, response):
        images = response.css('div.deviceoverviewsensorvalues a img::attr(src)').extract()
        uptd_name = response.css('div.deviceoverviewsensorvalues span a::text').extract()
        detail_urls = response.css('div.deviceoverviewsensorvalues a::attr(id)').extract()

        
        for idx, val in enumerate(zip(detail_urls, uptd_name, images), 1):
            yield response.follow('https://125.213.129.105/controls/sensorgraph.htm?id={}&graphid=2&columns=datetime,value_,coverage&Username=Diskominfo%20Jabar&Password=P4sswordJabar'.format(val[0]), self.parse_detail, meta={'seq_data': idx, 'uptd_name': val[1], 'uptd_id': val[0], 'img_url': val[2]})   

        # for idx, val in enumerate(zip(images, detail_urls, uptd_name)):
        #     scraped_info = {
        #         'idx_data': '{}'.format(idx),
        #         'image_urls' : 'https://125.213.129.105{}'.format(val[0]),
        #         'detail_urls' : val[1],
        #         'uptd_name' : val[2]
        #     }
        #     yield scraped_info


    def parse_detail(self, response):
        uptd_name = response.request.meta['uptd_name']
        uptd_id= response.request.meta['uptd_id']
        seq_data = response.request.meta['seq_data']
        img_data = response.request.meta['img_url']

        # detail data 
        lastscan = response.css('div.overviewsmalldata ul li span.overview-data span::text')[0].extract()
        lastup = response.css('div.overviewsmalldata ul li span.overview-data span::text')[1].extract()
        lastdown = response.css('div.overviewsmalldata ul li span.overview-data span::text')[2].extract()
        uptime = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[0].extract()
        downtime = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[1].extract()
        coverage = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[2].extract()
        sensortype = response.css('div.overviewsmalldata ul li span.overview-data::text')[0].extract()
        # label_data = response.css('div.overviewsmalldata ul li span.overview-title::text').extract()
        # img_data = response.css('div.PNGGraph img::attr(src)').get()

        res = requests.get("https://125.213.129.105/api/status.json?asjson=true&id={}&Username=Diskominfo%20Jabar&Password=P4sswordJabar".format(uptd_id), verify=False)
        jsonRes = res.json()

        detail_data = {
            'last_scan' : lastscan,
            'last_up' : lastup,
            'last_down' : lastdown,
            'uptime' : uptime,
            'downtime' : downtime,
            'coverage' : coverage,
            'sensortype' : sensortype,
            'downtimetime' : jsonRes['object']['downtimetime'],
            'interval' : jsonRes['object']['interval'],
            'name' : jsonRes['object']['name']
        }

        yield {
            'seq_number' : seq_data,
            'uptd_name' : uptd_name,
            'detail_data' : detail_data,
            'img_url' : 'https://125.213.129.105{}'.format(img_data)
        }