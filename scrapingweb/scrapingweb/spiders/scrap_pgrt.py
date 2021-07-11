import scrapy

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
        images = response.css('div.deviceoverviewsensorvalues a img::attr(src)').extract()
        uptd_name = response.css('div.deviceoverviewsensorvalues span a::text').extract()
        detail_urls = response.css('div.deviceoverviewsensorvalues a::attr(href)').extract()

        for idx, val in enumerate(zip(images, detail_urls, uptd_name)):
            scraped_info = {
                'idx_data': '{}'.format(idx),
                'image_urls' : 'https://125.213.129.105{}'.format(val[0]),
                'detail_urls' : 'https://125.213.129.105/{}&Username=Diskominfo%20Jabar&Password=P4sswordJabar'.format(val[1]),
                'uptd_name' : val[2]
            }
            
            yield scraped_info
        # # for i in response.css('div.prtg-box.prtg-plugin.maingraph a::attr(href)').getall():
        # #     data.append(i)
        # for i in response.css('div.deviceoverviewsensorvalues a img::attr(src)').getall():
        #     data.append(i)

        # #     data.append(i)
        # for i in response.css('div.deviceoverviewsensorvalues span a::text').getall():
        #     name.append(i)

        # for i in response.css('div.deviceoverviewsensorvalues a::attr(href)').getall():
        #     data.append(i)

        # for idx, val in enumerate(data):
        #     yield {
        #         name[idx]: 'https://125.213.129.105{}'.format(val)
        #     }
           

    # def parse_page(self, response):
  
    #     # Scraping all the items for all the reviewers mentioned on that Page
        
    #     names=response.xpath('//div[@data-hook="review"]//span[@class="a-profile-name"]/text()').extract()
    #     reviewerLink=response.xpath('//div[@data-hook="review"]//a[@class="a-profile"]/@href').extract()
    #     reviewTitles=response.xpath('//a[@data-hook="review-title"]/span/text()').extract()
    #     reviewBody=response.xpath('//span[@data-hook="review-body"]/span').xpath('normalize-space()').getall()
    #     verifiedPurchase=response.xpath('//span[@data-hook="avp-badge"]/text()').extract()
    #     postDate=response.xpath('//span[@data-hook="review-date"]/text()').extract()
    #     starRating=response.xpath('//i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()').extract()
    #     helpful = response.xpath('//span[@class="cr-vote"]//span[@data-hook="helpful-vote-statement"]/text()').extract()
        
    #     # Extracting details of each reviewer and storing it in in the MyItem object items and then appending it to the JSON file.
        
    #     for (name, reviewLink, title, Review, Verified, date, rating, helpful_count) in zip(names, reviewerLink, reviewTitles, reviewBody, verifiedPurchase, postDate, starRating, helpful):
            
    #         # Getting the Next Page URL for futher scraping.
    #         next_urls = response.css('.a-last > a::attr(href)').extract_first()
            
    #         yield MyItem(names=name, reviewerLink = reviewLink, reviewTitles=title, reviewBody=Review, verifiedPurchase=Verified, postDate=date, starRating=rating, helpful=helpful_count, nextPage=next_urls)

    #     # This will get the next psge URL
    #         next_page = response.css('.a-last > a::attr(href)').extract_first()
    #         # Checking if next page is not none then loop back in the same function with the next page URL.
    #         if next_page is not None:
    #             yield response.follow("https://www.amazon.in"+next_page, callback=self.parse_page)
