import scrapy
import requests
import logging
from operator import itemgetter
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.pipelines.images import ImagesPipeline
from ... scrapingweb.items import ScrapingwebItem
from ... scrapingweb.items import ImageItem


class ReviewspiderSpider(scrapy.Spider):
    name = 'pgrt'
    start_urls = ['https://125.213.129.105/controls/objectgraph.htm?id=0&graphid=2&columns=datetime,value_,coverage&_=1625796838093&Username=Diskominfo%20Jabar&Password=P4sswordJabar']
    # quotation_mark_pattern = re.compile(r'“|”')

    def parse(self, response):
        item = ScrapingwebItem()
        images = response.css('div.deviceoverviewsensorvalues a img::attr(src)').extract()[4::]
        uptd_name = response.css('div.deviceoverviewsensorvalues span a::text').extract()[4::]
        detail_urls = response.css('div.deviceoverviewsensorvalues a::attr(id)').extract()[4::]

        
        for idx, val in enumerate(zip(detail_urls, uptd_name, images), 1):
            yield response.follow('https://125.213.129.105/controls/sensorgraph.htm?id={}&graphid=2&columns=datetime,value_,coverage&Username=Diskominfo%20Jabar&Password=P4sswordJabar'.format(val[0]), self.parse_detail, meta={'seq_data': idx, 'uptd_name': val[1], 'uptd_id': val[0], 'img_url': val[2], 'item': item})   

    def parse_detail(self, response):
        uptd_name = response.request.meta['uptd_name']
        uptd_id= response.request.meta['uptd_id']
        seq_data = response.request.meta['seq_data']
        img_url = response.request.meta['img_url']
        item = response.request.meta['item']
        # detail data 
        lastscan = response.css('div.overviewsmalldata ul li span.overview-data span::text')[0].extract()
        lastup = response.css('div.overviewsmalldata ul li span.overview-data span::text')[1].extract()
        lastdown = response.css('div.overviewsmalldata ul li span.overview-data span::text')[2].extract()
        uptime = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[0].extract()
        downtime = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[1].extract()
        coverage = response.css('div.overviewsmalldata ul li span.overview-data dummy::text')[2].extract()
        sensortype = response.css('div.overviewsmalldata ul li span.overview-data::text')[0].extract()
        averageSpeed = response.css("div #table_valuetable2 tr.averages td::text").extract()[2]
        # label_data = response.css('div.overviewsmalldata ul li span.overview-title::text').extract()
        # img_data = response.css('div.PNGGraph img::attr(src)').get()

        res = requests.get("https://125.213.129.105/api/status.json?asjson=true&id={}&Username=Diskominfo%20Jabar&Password=P4sswordJabar".format(uptd_id), verify=False)
        jsonRes = res.json()

        # Traffic Total (speed) = Speed Average
        # Traffic in 

        detail_data = {
            'last_scan' : lastscan,
            'last_up' : lastup,
            'last_down' : lastdown,
            'uptime' : uptime,
            'downtime' : downtime,
            'coverage' : coverage,
            'sensortype' : sensortype,
            'average_speed': averageSpeed,
            'downtimetime' : jsonRes['object']['downtimetime'],
            'interval' : jsonRes['object']['interval'],
            'name' : jsonRes['object']['name'],
            'bandwith' : '600,000 KB'
        }

        self.quotes_list.append({
            'seq_number' : seq_data,
            'uptd_name' : uptd_name,
            'detail_data' : detail_data,
            'img_url' : 'https://125.213.129.105{}'.format(img_url),
            'address' : 'Jl. Dipenogoro No.22 Citarum, Kec. Bandung Wetan, Kota Bandung, Jawa Barat 40115',
            })
        
        # item['image_urls'] = 'https://125.213.129.105{}'.format(img_url)

        # yield ImageItem(image_urls=[img_url])
        # yield {
        #     'seq_number' : seq_data,
        #     'uptd_name' : uptd_name,
        #     'detail_data' : detail_data,
        #     'img_url' : 'https://125.213.129.105{}'.format(img_data),
        #     'address' : 'Jl. Dipenogoro No.22 Citarum, Kec. Bandung Wetan, Kota Bandung, Jawa Barat 40115',
        # }
