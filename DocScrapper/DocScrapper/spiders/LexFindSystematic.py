import scrapy
from scrapy import Request
from scrapy.http import JsonRequest
import requests
from datetime import datetime, timezone
from Connections.AzureDataLake import AzureStorageManager
from hashlib import sha256
from DocScrapper.items import PdfMetaData
import json
import logging
from urllib.parse import urlencode
from PyPDF2 import PdfReader
import io
logger = logging.getLogger(__name__)

START_URL = 'https://www.lexfind.ch/api/fe/de/global/systematics'

WEB_CONFIG = json.load(open('DocScrapper\lex_find_web_config.json'))

INIT_PARAMS = WEB_CONFIG['params']

HEADERS = WEB_CONFIG['headers']

PDF_HEADERS = WEB_CONFIG['pdf_headers']

LANGUAGES = ['it', 'de', 'fr']

BASE_URL = "https://www.lexfind.ch/api/fe/de/global/systematics?active_only=false&category_filter%5B%5D=1&category_filter%5B%5D=2&category_filter%5B%5D=3&category_filter%5B%5D=4&category_filter%5B%5D=5&category_filter%5B%5D=6&category_filter%5B%5D=7&category_filter%5B%5D=8&category_filter%5B%5D=9&entity_filter%5B%5D=1&entity_filter%5B%5D=10&entity_filter%5B%5D=11&entity_filter%5B%5D=12&entity_filter%5B%5D=13&entity_filter%5B%5D=14&entity_filter%5B%5D=15&entity_filter%5B%5D=16&entity_filter%5B%5D=17&entity_filter%5B%5D=18&entity_filter%5B%5D=19&entity_filter%5B%5D=2&entity_filter%5B%5D=20&entity_filter%5B%5D=21&entity_filter%5B%5D=22&entity_filter%5B%5D=23&entity_filter%5B%5D=24&entity_filter%5B%5D=25&entity_filter%5B%5D=26&entity_filter%5B%5D=27&entity_filter%5B%5D=28&entity_filter%5B%5D=3&entity_filter%5B%5D=4&entity_filter%5B%5D=5&entity_filter%5B%5D=6&entity_filter%5B%5D=7&entity_filter%5B%5D=8&entity_filter%5B%5D=9&tols_for_systematics%5B%5D={tols_id}"

 
class LexfindsystematicSpider(scrapy.Spider):
    name = "LexFindSystematic"
    allowed_domains = ["www.lexfind.ch"]

    def __init__(self):
        
        self.blob_storage_manager = AzureStorageManager()
        super(LexfindsystematicSpider, self).__init__()

    def start_requests(self):
        """Get the initial mapper"""
        
        yield Request(
                url = f'{START_URL}?{urlencode(INIT_PARAMS, doseq=True)}',
                headers=HEADERS,
                 callback=self.mapper_requests,
             )

    def mapper_requests(self,response):
        """Using the mapper add """
        try:
            MAPPER = response.json() 
        except requests.exceptions.RequestException as e:
            logger.error(f"Something went wrong with requesting MAPPER, or did not receive Json in mapper_requests: {e}")

        for key in MAPPER.keys() :
             
            yield JsonRequest(
                url = BASE_URL.format(tols_id=key),
                headers=HEADERS,
                callback=self.parse_page,
                cb_kwargs={
                    "tols_id": key
                },
                method="GET"
            )

    def parse_page(self, response, tols_id):
        """From the tols in the response iterate on the pattern to create the link where we can find the download link, this is for metadata only
           As well as the version url which will be used to get the id for the download link for the latest pdf"""
        
        response = response.json()[tols_id]
        tols = response['tols']

        for tols_item in tols:
            for language in LANGUAGES:
                page_pdf_url = f"https://www.lexfind.ch/fe/{language}/tol/{tols_item['id']}/{language}"
                version_url = f"https://www.lexfind.ch/api/fe/{language}/texts-of-law/{tols_id}/with-version-groups"
                meta_data = {
                        "id": tols_item['id'],
                        "title" : tols_item['title'],
                        "systematic_number" : tols_item['systematic_number'],
                        "language" : language,
                        "page_pdf_url" : page_pdf_url,
                        "version_url" : version_url
                        }
                yield Request(
                    version_url,
                    callback=self.enrich_meta_and_parse_pdf,
                    cb_kwargs={
                 
                    "meta_data": meta_data
                } 
                )

    def enrich_meta_and_parse_pdf(self, response, meta_data) -> PdfMetaData:
        """This processing function retreives additional metada,
            creates the pdf download link,
            download and upload the pdf,
            and upserts metadata to MONGODB"""
        
        #reteive latest version of pdf, to get dates, and id
        version_meta_data = response.json()['families'][0][0][0]
        meta_data['version_initial_date'] = version_meta_data['version_active_since']
        meta_data['version_last_update'] = version_meta_data['version_active_since']
        
        #get id from latest version , and create the download link
        latest_pdf_sys_id = version_meta_data['id']
        pdf_download_url = f"https://www.lexfind.ch/tolv/{latest_pdf_sys_id}/{meta_data['language']}"
        meta_data['pdf_download_url'] = pdf_download_url

        #download and hash the pdf
        yield   Request (pdf_download_url, 
                         headers= PDF_HEADERS,
                         callback= self.parse_pdf,
                           cb_kwargs={
                                    "meta_data": meta_data
                                    }
                  )


    def parse_pdf(self, response, meta_data):
        
        pdf_binary = response.body
        
        # check if pdf is valid and hash it.
        meta_data['is_valid_pdf'] = PdfReader(io.BytesIO(pdf_binary)).pages and True
        meta_data['pdf_content_hash'] = sha256(pdf_binary).hexdigest()

        #get month year in order to upload to a corresponding folder
        _, month, year = meta_data['version_last_update'].split('.')
        
        # create upload link, and upload pdf
        blob_storage_relative_path = f"{meta_data['language']}/{year}/{month}/{meta_data['pdf_content_hash']}.pdf"
        meta_data['blob_relative_path'] = blob_storage_relative_path
        self.blob_storage_manager.upload_data(pdf_binary, blob_storage_relative_path)
        meta_data['ts_inserted'] = datetime.now(timezone.utc)
        
        # copy metadata to PdfMetadata and yield it.
        item =PdfMetaData()
        item.update(meta_data)
        yield item
 
