import scrapy
from scrapy import Request
from scrapy.http import JsonRequest
import requests
from datetime import datetime, timezone
from Connections.AzureDataLake import AzureStorageManager
from hashlib import sha256
from DocScrapper.items import PdfMetaData
import json

WEB_CONFIG = json.load(open('DocScrapper\lex_find_web_config.json'))

INIT_PARAMS = WEB_CONFIG['params']

HEADERS = WEB_CONFIG['headers']

PDF_HEADERS = WEB_CONFIG['pdf_headers']

MAPPER = json.loads(requests.get('https://www.lexfind.ch/api/fe/de/global/systematics', params= INIT_PARAMS , headers= HEADERS).content)

LANGUAGES = ['de', 'it', 'fr']

BASE_URL = "https://www.lexfind.ch/api/fe/de/global/systematics?active_only=false&category_filter%5B%5D=1&category_filter%5B%5D=2&category_filter%5B%5D=3&category_filter%5B%5D=4&category_filter%5B%5D=5&category_filter%5B%5D=6&category_filter%5B%5D=7&category_filter%5B%5D=8&category_filter%5B%5D=9&entity_filter%5B%5D=1&entity_filter%5B%5D=10&entity_filter%5B%5D=11&entity_filter%5B%5D=12&entity_filter%5B%5D=13&entity_filter%5B%5D=14&entity_filter%5B%5D=15&entity_filter%5B%5D=16&entity_filter%5B%5D=17&entity_filter%5B%5D=18&entity_filter%5B%5D=19&entity_filter%5B%5D=2&entity_filter%5B%5D=20&entity_filter%5B%5D=21&entity_filter%5B%5D=22&entity_filter%5B%5D=23&entity_filter%5B%5D=24&entity_filter%5B%5D=25&entity_filter%5B%5D=26&entity_filter%5B%5D=27&entity_filter%5B%5D=28&entity_filter%5B%5D=3&entity_filter%5B%5D=4&entity_filter%5B%5D=5&entity_filter%5B%5D=6&entity_filter%5B%5D=7&entity_filter%5B%5D=8&entity_filter%5B%5D=9&tols_for_systematics%5B%5D={tols_id}"

class LexfindsystematicSpider(scrapy.Spider):
    name = "LexFindSystematic"
    allowed_domains = ["www.lexfind.ch"]

    def __init__(self):


        self.blob_storage_manager = AzureStorageManager()

        super(LexfindsystematicSpider, self).__init__()

    def start_requests(self):
 
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
 
        response = response.json()[tols_id]
        tols = response['tols']

        for tols_item in tols:
            # print(tols_item)
            for language in LANGUAGES:
                page_pdf_url = f"https://www.lexfind.ch/fe/de/tol/{tols_item['id']}/{language}"
                version_url = f"https://www.lexfind.ch/api/fe/de/texts-of-law/{tols_id}/with-version-groups"
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
                    callback=self.parse,
                    cb_kwargs={
                    "tols_id" : tols_id,
                    "meta_data": meta_data
                } 
                )

    def parse(self, response, tols_id, meta_data) -> PdfMetaData:
        item =PdfMetaData()
        version_meta_data = response.json()['families'][0][0][0]
        meta_data['version_initial_date'] = version_meta_data['version_active_since']
        meta_data['version_last_update'] = version_meta_data['version_active_since']
         
        latest_pdf_sys_id = version_meta_data['id']
        pdf_download_url = f"https://www.lexfind.ch/tolv/{latest_pdf_sys_id}/{meta_data['language']}"
        meta_data['pdf_download_url'] = pdf_download_url

        pdf_binary = requests.get(pdf_download_url, headers= PDF_HEADERS).content
        meta_data['pdf_content_hash'] = sha256(pdf_binary).hexdigest()

        _, month, year = meta_data['version_last_update'].split('.')

        blob_storage_relative_path = f"{meta_data['language']}/{year}/{month}/{meta_data['pdf_content_hash']}.pdf"
        meta_data['blob_relative_path'] = blob_storage_relative_path
        self.blob_storage_manager.upload_data(pdf_binary, blob_storage_relative_path)
        meta_data['ts_inserted'] = datetime.now(timezone.utc)

        item =PdfMetaData()
        item.update(meta_data)
        yield item
 
