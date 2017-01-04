import os
import urllib.request
from scrapy.spiders import Spider
from scrapy.http import Request
from seCrawler.common.searResultPages import searResultPages
from seCrawler.common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import Selector
from scrapy.cmdline import execute


class keywordSpider(Spider):
    name = 'keywordSpider'
    allowed_domains = ['bing.com','google.com','baidu.com']
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None

    def __init__(self, keyword, se='bing', pages=20,  *args, **kwargs):
        # super(keywordSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword.lower() # document filetype:pdf
        self.searchEngine = se.lower()
        self.selector = SearchEngineResultSelectors[self.searchEngine]
        pageUrls = searResultPages(keyword, se, int(pages))
        for url in pageUrls:
            print(url)
            self.start_urls.append(url)

    def parse(self, response):

        for url in Selector(response).xpath(self.selector).extract():
            yield Request(
                url,
                callback=self.save_pdf,
                errback=self.handle_error,
                dont_filter=True
            )
            print(url)

        pass

    def handle_error(self, failure):
        self.log("Request failed: %s" % failure.request)

    def save_pdf(self, response):

        url = response.url

        # calculate file download size in byte
        pdf_file_size = urllib.request.urlopen(url).info()['content-length']
        print('File size: ' + pdf_file_size)

        # limit of the downloaded size of pdf file
        if int(pdf_file_size) < 12000000:
            # folder_path = os.path.join('Users', 'jan.nehmiz', 'Documents', 'Automated UI Testing', 'Template Files')
            folder_path = '/Users/jan.nehmiz/Documents/Automated UI Testing/Template Files/'
            filename = url.split('/')[-1]
            path = folder_path + filename

            self.logger.info('Saving PDF %s', path)
            with open(path, 'wb') as f:
                f.write(response.body)
        else:
            print('Not saved')






