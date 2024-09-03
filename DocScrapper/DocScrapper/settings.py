import os
# Scrapy settings for DocScrapper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


user = os.getenv("MONGODB_USER")
password = os.getenv("MONGODB_PASSWORD")
# pwd = urllib.parse.quote_plus(password) # in case the password needs the be parsed
host = os.getenv("MONGODB_HOST")
MONGO_URI = f"mongodb://{user}:{password}@{host}:27017/?authMechanism=DEFAULT"
MONGO_DATABASE = os.getenv("MONGODB_DATABASE")


BOT_NAME = "DocScrapper"

SPIDER_MODULES = ["DocScrapper.spiders"]
NEWSPIDER_MODULE = "DocScrapper.spiders"

LOG_FILE = 'crawler.log'
LOG_LEVEL = 'INFO'

ROBOTSTXT_OBEY = True
DOWNLOAD_HANDLERS = {
"http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
"https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"
 
 
AZURE_ACCOUNT_URL = f"https://{os.getenv('AZURE_ACCOUNT_NAME')}.blob.core.windows.net/"
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")


ITEM_PIPELINES = {
   "DocScrapper.pipelines.MongoDBPipeline": 300,
 
}

DOWNLOADER_MIDDLEWARES = {
   "DocScrapper.middlewares.DocscrapperSpiderMiddleware": 543,
}