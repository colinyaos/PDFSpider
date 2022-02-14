import scrapy
import requests
import os
import urllib.parse as up

class PDFSpider(scrapy.Spider):
    name = "PDFSpider"

    start_urls = [
        'https://cms.math.ca/competitions/cmo/',
    ]

    def __init__(self, url = start_urls[0], *args, **kwargs):
        super(PDFSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        origin_url = self.start_urls[0]
        origin_url_parse = up.urlparse(origin_url)

        origin_url_parse._replace(path = None)

        base_url = up.urlunparse(origin_url_parse)

        for pdf_url in response.xpath("//a[contains (@href, '.pdf')]/@href").getall():

            item_url = up.urljoin(base_url, pdf_url)
            # This deals with both absolute and relative paths by merging with 
            # the original url. 
            
            try:
                r = requests.get(item_url, stream = True)
            except Exception as e:
                print(f"Invalid URL passed, {e}.")
                pass

            parsed_item_url = up.urlparse(item_url)
            
            pdf_name = parsed_item_url.path

            pdf_name = pdf_name.strip("/")
            pdf_name = pdf_name.replace("/", "-") 
            # I thought it better to avoid using slashes in filenames. 





            write_dir = os.path.join(os.getcwd(), "Math Problems")
            # Writes to the "PDFs" directory in PDFSpider's home dir. 
            # To change, simply reconfigure the relative path. 

            with open(os.path.join(write_dir, pdf_name),"wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    # writing one chunk at a time to pdf file
                    if chunk:
                        pdf.write(chunk)

            yield {
                'url': pdf_url,
            }