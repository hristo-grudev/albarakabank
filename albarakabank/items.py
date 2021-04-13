import scrapy


class AlbarakabankItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
