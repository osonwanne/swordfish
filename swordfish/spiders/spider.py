import scrapy, time, logging
from swordfish.items import SwordfishItem


class MySpider(scrapy.Spider):
    name = 'swordfish'
    # handle_httpstatus_list = [302]

    start_urls = ['https://www.yelp.com/search?find_desc=Seafood+Restaurant&find_loc=Boston,+MA']
    # https://www.yelp.com/search?find_desc=Seafood+Restaurant&find_loc=Honolulu,+HI
    # https://www.yelp.com/search?find_desc=Seafood+Restaurant&find_loc=New+York,+NY
    

    def parse(self, response):
        urls = response.css('.indexed-biz-name .biz-name::attr(href)').extract()
        for url in urls:
            request = scrapy.Request(response.urljoin(url) , callback=self.parse_page)
            yield request

        nextpage = response.xpath('//a[contains(@class,"u-decoration-none next pagination-links_anchor")]/@href').extract_first()
        request1 = scrapy.Request(response.urljoin(nextpage))
        yield request1

    def parse_page(self, response):
        item = SwordfishItem()
        name = response.xpath('//h1[@class="biz-page-title embossed-text-white"]/text()').extract_first()
        menu = ""
        if response.xpath('//a[@class="external-menu js-external-menu"]/@href').extract_first():
            menu = str(response.xpath('//a[@class="external-menu js-external-menu"]/@href').extract_first()).split('url=')[-1].replace('%3A',':').replace('%2F','/').replace('&website_link_type=menu','')
        elif response.xpath('//a[@class="menu-explore js-menu-explore"]/@href').extract_first():
            menu = response.xpath('//a[@class="menu-explore js-menu-explore"]/@href').extract_first()
            menu = "https://www.yelp.com" + menu
        else:
            menu = ""
        item['name'] = self.manual(name)
        item['url'] = self.manual(response.url)
        item['menu'] = self.manual(menu)
        if menu: # and '.pdf' not in menu:
            yield scrapy.Request(menu, callback=self.parse_menu, meta={"item": item})
        else:
            item['swordfish'] = "False"
			# return item

    def parse_menu(self, response):
        item = response.meta["item"]
        if response.xpath('//*[contains(text(),"Swordfish") or contains(text(),"SwordFish") or contains(text(),"SWORDFISH") or contains(text(),"swordfish")]/text()').extract():
            item['swordfish'] = "True"
        else:
            item['swordfish'] = "False"
        return item


    def manual(self,var_str):
        if var_str is None:
            return ""
        return var_str.strip().rstrip()
