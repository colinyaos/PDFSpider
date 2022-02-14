from http.client import InvalidURL
import scrapy
import requests
import os
import urllib.parse as up

class PDFSpider(scrapy.Spider):
    name = "PDFSpider"
    # start_urls = [
    #     'https://www.hmmt.org/www/archive/251',
    # ]

    # start_urls = [
    #     'https://cms.math.ca/competitions/cmo/',
    # ]

    start_urls = [
        'https://www1.nyc.gov/site/nypd/about/about-nypd/manual.page',
    ]

    def parse(self, response):
        origin_url = self.start_urls[0]
        origin_url_parse = up.urlparse(origin_url)
        print("\n", origin_url_parse.scheme, origin_url_parse.hostname, origin_url_parse.path, "\n")

        origin_url_parse._replace(path = None)
        print("\n", origin_url_parse.scheme, origin_url_parse.hostname, origin_url_parse.path, "\n")

        base_url = up.urlunparse(origin_url_parse)

        for pdf_url in response.xpath("//a[contains (@href, '.pdf')]/@href").getall():


            target_url = up.urlparse(pdf_url)

            print("\n", "scheme:", target_url.scheme, "netloc", target_url.netloc, "path", target_url.path, "\n")


            new_url = up.urljoin(base_url, pdf_url)

            target_url = up.urlparse(new_url)
            print("\n", "scheme:", target_url.scheme, "netloc", target_url.netloc, "path", target_url.path, "\n")

            item_url = up.urlunparse(target_url)

            print(item_url)

            
            try:
                r = requests.get(item_url, stream = True)
            except Exception as e:
                print(f"Invalid URL passed, {e}.")
                pass



            domain_extensions = [".com", ".org", ".net", ".gov", ".ca"]

            website_end_token = 200 # the longest web address is less than 100 chars, 
            # so this should always work. 

            print("Trying to parse domain extensions. \n\n")

            for e in domain_extensions:
                try:
                    website_end_token = min(item_url.index(e), website_end_token)
                except ValueError:
                    # print("Not a valid website. ")        
                    pass        

            if website_end_token == 200: 
                # This implies that the website ending follows none of the endings given above. 
                print("Website ending invalid. ")
                return

            # website_end_token = item_url.index(".com")
            # print(website_end_token, "\n\n")
            

            pdf_name = item_url[website_end_token + item_url[website_end_token:].index("/") + 1:]
            pdf_name = pdf_name.replace("/", "-")

            print(pdf_name)

            write_dir = os.path.join(os.getcwd(), "PDFs")

            with open(os.path.join(write_dir, pdf_name),"wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
            
                    # writing one chunk at a time to pdf file
                    if chunk:
                        pdf.write(chunk)

            yield {
                'url': pdf_url,
            }