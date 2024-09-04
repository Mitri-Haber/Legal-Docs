# Scraping Pdf Metadata and pdf downloader for LexFind
# (https://www.lexfind.ch/fe/de/systematic)

## 1. Architecture
### The architecture is described as below:
- **1.1: spiders**: 
    -  Request a mapper used by the javascript request for url automation
    -  Iterate over the elements of the mapper to get to pages and collect metadata 
    -  Iterare over pdf landing pages, while taking in cosinderation the latest version of pdf , and enrich metadata, Download pdfs 
    -  Enrich metadata, upload pdf to azure blob, and upsert Metada
- **1.2: pipelines**
    - Pipline to handle upserting pdf metada in MongoDB that have ts_upserted and upser_counter
    - External Azure blob connector called from spiders
- **1.3: middleware**:
    - To pre-and-post process requests and responses
- **1.4: Logger**:
    - Logging important and blockers using Scrapy's logging process

 
## 2. How to Run
### **2.1: Credentials**
- Remove *.example* from ***.env.example*** file and fill in the variables.

``` Python
#Mongdo DB credentials
MONGODB_USER = ''
MONGODB_PASSWORD = ''
MONGODB_HOST = ''
MONGODB_PORT = 
MONGODB_DATABASE = ''

#Azure blob storage info
AZURE_ACCOUNT_NAME = ''
AZURE_CONTAINER_NAME = ''
AZURE_ACCOUNT_KEY = ''
```
### **2.2: Run**

Clone the projec using Git Bash, cd to root directory and create a python virtual environment
```
$ python -m venv .venv
```
Activate the venv

```
$ venv/Scripts/Activate (Linux)
$ source venv/bin/activate (Windows)
```



Install the requirements
```
$ pip install -r requirements.txt
```
Navigate to DocScrapper project
```
 cd .\DocScrapper (windows)
 cd ./DocScrapper (linux)
```
Run the Crawler
```
$ scrapy crawl LexFindSystematic
```
