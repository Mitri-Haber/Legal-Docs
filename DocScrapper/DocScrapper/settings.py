import os
# Scrapy settings for DocScrapper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "DocScrapper"

SPIDER_MODULES = ["DocScrapper.spiders"]
NEWSPIDER_MODULE = "DocScrapper.spiders"

LOG_FILE = 'crawler.log'
LOG_LEVEL = 'INFO'

#Mongo connection string and DAtabase to be used
MONGO_URI = f'mongodb://{os.getenv("MONGODB_USER")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_HOST")}:27017/?authMechanism=DEFAULT'
MONGO_DATABASE = os.getenv("MONGODB_DATABASE")

#Azure blob connection string
AZURE_ACCOUNT_URL = f"https://{os.getenv('AZURE_ACCOUNT_NAME')}.blob.core.windows.net/"
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")

ROBOTSTXT_OBEY = True
DOWNLOAD_HANDLERS = {
"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
"https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
 
#Mongo db pipline to handle upserts
ITEM_PIPELINES = {
   "DocScrapper.pipelines.MongoDBPipeline": 300,
 
}

DOWNLOADER_MIDDLEWARES = {
   "DocScrapper.middlewares.DocscrapperSpiderMiddleware": 543,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"