from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from test_scrapy.items import TestScrapyItem

class WoblogSpider(BaseSpider):
    name = "woblog"
    allowed_domains = ["tetsuwo.tumblr.com"]
    start_urls = ["http://tetsuwo.tumblr.com"]

    def parse(self, response):
        hxs = HtmlXPathSelector(request)

        next_page = hxs.select("//div[@class='pagination']/a[@class='next_page']/@href").extract()
        if not not next_page:
            yield Request(next_page[0], self.parse)

        posts = hxs.select("//div[@class='post']")
        items = []
        for post in posts:
            item = TestScrapyItem()
            item["title"] = post.select("//div[@class='bodytext']/h2/a/text()").extract()
            item["link"] = post.select("//div[@class='bodytext']/h2/a/@href").extract()
            item["content"] = post.select("//div[@class='bodytext']/p/text()").extract()
            items.append(item)
        for item in items:
            yield item
