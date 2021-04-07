import scrapy

from scrapy.loader import ItemLoader

from ..items import ArmstrongItem
from itemloaders.processors import TakeFirst


class ArmstrongSpider(scrapy.Spider):
	name = 'armstrong'
	start_urls = ['https://www.armstrong.bank/connect/news-and-updates']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-item-text"]')
		for post in post_links:
			url = post.xpath('.//a[@data-link-type-id="page"]/@href').get()
			date = post.xpath('.//div[@class="news-item-text-date"]//text()[normalize-space()]').get()
			if url:
				yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mb-6", " " ))]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ArmstrongItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
