import scrapy

from scrapy.loader import ItemLoader

from ..items import AlbarakabankItem
from itemloaders.processors import TakeFirst


class AlbarakabankSpider(scrapy.Spider):
	name = 'albarakabank'
	start_urls = ['https://www.albaraka-bank.com.eg/%D8%A7%D9%84%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1.aspx']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="headline"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//*[(@id = "content")]//span/text()').get()
		description = response.xpath('//p[@dir="RTL"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AlbarakabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
