import scrapy
import requests
import logging

class MyItem(scrapy.Item):
    images = scrapy.Field()
    nextPage = scrapy.Field(default = 'null')

class ReviewspiderSpider(scrapy.Spider):
    name = 'pgrt'
    start_urls=[
        "https://125.213.129.105/controls/objectgraph.htm?id=0&graphid=2&columns=datetime,value_,coverage&_=1625796838093&Username=Diskominfo%20Jabar&Password=P4sswordJabar"
        # "https://125.213.129.105/controls/objectgraph.htm?id=0&graphid=3&columns=datetime,value_,coverage&_=1625796838093&Username=Diskominfo%20Jabar&Password=P4sswordJabar",
    ]

    def parse(self, response):
        # images = response.css('div.deviceoverviewsensorvalues a img::attr(src)').extract()
        uptd_name = response.css('div.deviceoverviewsensorvalues span a::text').extract()
        detail_urls = response.css('div.deviceoverviewsensorvalues a::attr(id)').extract()

        
        for idx, val in enumerate(zip(detail_urls, uptd_name)):
            yield response.follow('https://125.213.129.105/controls/sensorgraph.htm?id={}&graphid=2&columns=datetime,value_,coverage&Username=Diskominfo%20Jabar&Password=P4sswordJabar'.format(val[0]), self.parse_detail, meta={'uptd_name': val[1], 'uptd_id': val[0]})   

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
        # detail_data = response.css('div.overviewsmalldata ul li span.overview-data::text').extract()
        # label_data = response.css('div.overviewsmalldata ul li span.overview-title::text').extract()
        img_data = response.css('div.PNGGraph img::attr(src)').get()
        detail_data = []

        res = requests.get("https://125.213.129.105/api/status.json?asjson=true&id={}&Username=Diskominfo%20Jabar&Password=P4sswordJabar".format(uptd_id), verify=False)
        jsonRes = res.json()

        detail_data = {
            'last_scan' : jsonRes['object']['lastcheck'],
            'last_up' : jsonRes['object']['lastup'],
            'last_down' : jsonRes['object']['lastdown'],
            'uptime' : jsonRes['object']['uptime'],
            'downtime' : jsonRes['object']['downtime'],
            'downtimetime' : jsonRes['object']['downtimetime'],
            'coverage' : jsonRes['object']['coverage'],
            'coveragetime' : jsonRes['object']['coveragetime'],
            'interval' : jsonRes['object']['interval'],
            'sensortype' : jsonRes['object']['sensortype'],
            'name' : jsonRes['object']['name']
        }

        yield { 
            'uptd_name' : uptd_name,
            'detail_data' : detail_data,
            'img_url' : 'https://125.213.129.105{}&Username=Diskominfo%20Jabar&Password=P4sswordJabar'.format(img_data)
        }