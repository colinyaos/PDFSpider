import scrapy

class PDFSpider(scrapy.Spider):
    name = "PDFSpider"
    start_urls = [
        'https://www.hmmt.org/www/archive/251',
    ]

    def parse(self, response):
        for pdf_url in response.css('a::attr(href)').re(r'.*.pdf'):
            print(pdf_url)
            yield {
                'url': pdf_url,
            }

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)