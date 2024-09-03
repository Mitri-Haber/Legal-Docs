# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PdfMetaData(scrapy.Item):
    
    id = scrapy.Field()
    title = scrapy.Field()
    systematic_number = scrapy.Field()
    language = scrapy.Field()
    page_pdf_url = scrapy.Field()
    version_url = scrapy.Field()
    version_initial_date = scrapy.Field()
    version_last_update = scrapy.Field()
    pdf_download_url = scrapy.Field()
    pdf_content_hash = scrapy.Field()
    blob_relative_path = scrapy.Field()
    ts_inserted = scrapy.Field()
