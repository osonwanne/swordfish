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

	# def parse_page(self, response):
	# 	item = SwordfishItem()

	#     name = response.xpath('//h1[@class="biz-page-title embossed-text-white shortenough"]/text()').extract_first()
	    
	#     #introduce case or if/else
	#     menu = response.xpath('//a[@class="external-menu js-external-menu"]/@href').extract_first()

	#     # menu = response.xpath('//a[@class="menu-explore js-menu-explore"]/@href').extract_first()
	#     # menu = "www.yelp.com"+menu

	#     #click on full menu link


	#     swordfish = response.xpath('//li[@id="region-zipcode"]/a/text()').extract_first()

	#     item['name'] = self.manual(name)
	#     item['url'] = self.manual(response.url)
	#     item['menu'] = self.manual(menu)
	#     item['swordfish'] = self.manual(swordfish)

	#     return item


    def manual(self,var_str):
        if var_str is None:
            return ""
        return var_str