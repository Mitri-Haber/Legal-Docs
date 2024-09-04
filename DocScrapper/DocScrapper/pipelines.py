import os, logging
import pymongo
import scrapy
from itemadapter import ItemAdapter
from DocScrapper.items import PdfMetaData
from datetime import datetime



logger = logging.getLogger(__name__)

class MongoDBPipeline(object):

    # MongoDB collection name
    collection_name = os.getenv("SOURCE_HOST")

    def __init__(self, mongo_uri, mongo_db) -> None:
        """ Assigns the mongo uri and db name after getting them
           from the classmethod"""
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """ Create the instance with mongo_uri and mongo_db
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )
    
    def open_spider(self, spider) -> None:
        """ When the spider is opened, a MongoDB connector instance is
            created and the connection is opened.
        """
        logger.info('Connecting to MongoDB.')
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider) -> scrapy.Item:
        """ Gets the  item and upsets in mongodb
        """
        logger.info(f"Upserting Metadata for {item['pdf_download_url']} ")
        
        data =  ItemAdapter(item).asdict()
        rule = {"pdf_content_hash" : data['pdf_content_hash']}
        
        existing_document =  self.db[self.collection_name].find_one(rule)
        
        if existing_document is None:
            data['ts_updated'] = None
        else:
            data['ts_updated'] = datetime.utcnow()
            data['update_counter'] = 1 + existing_document.get('update_counter', 0) 
 
        self.db[self.collection_name].update_one(rule, {"$set": data}, upsert=True)
        return item

    def close_spider(self, spider) -> None:
 
 
        self.client.close()
