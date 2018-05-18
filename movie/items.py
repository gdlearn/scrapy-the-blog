import scrapy
 
 
class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title=scrapy.Field()
   	cat_url=scrapy.Field()
   	detail_url=scrapy.Field()
   	views=scrapy.Field()
   	title=scrapy.Field()
   	content=scrapy.Field()
  