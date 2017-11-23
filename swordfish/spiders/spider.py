import scrapy, time
from swordfish.items import SwordfishItem


class MySpider(scrapy.Spider):
    name = 'swordfish'
    allowed_domains = ['yelp.com']
    
    start_urls = ['https://www.yelp.com/search?find_desc=Seafood+Restaurant&find_loc=Honolulu,+HI']

    # end start_urls

    def parse(self, response):    
	    urls = response.xpath('//ul[@class="ylist ylist-bordered search-results yloca-pills-blue yloca-wrapper-grey"]/li/div/div/div/div/div/h3/span/a/@href').extract()
	    for url in urls:            
	        request = scrapy.Request(response.urljoin(url) , callback=self.parse_page)      
	        yield request

	    nextpage = response.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract_first() 
	    request1 = scrapy.Request(response.urljoin(nextpage))
	    yield request1