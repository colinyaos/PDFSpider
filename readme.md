Readme for PDFSpider

To use: 
Run the command "scrapy crawl PDFSpider" in the top-level directory of PDFSpider (the one containing "Math Problems"). The files downloaded by the spider will be located in this folder. 

Additionally, by adding the additional argument '-a url="%URLNAME"', pdfs can be downloaded from webpages apart from the default CMO webpage. 
ex. "scrapy crawl PDFSpider -a url="https://www.hmmt.org/www/archive/251". 
These pdfs will also be written to the same "Math Problems" directory. 


I've never worked with web spiders before, and scraping these files was a new experience for me. There is likely a better way to write these files using scrapy's own Pipeline structures, and my use of xpath to grab .pdfs directly feels a little heavy-handed, where a filtering system in Beautiful Soup might have worked better. I also assumed that addresses given in mrefs would be well-formed, which could lead to issues down the line. Still, I think I did the best I could, given the limited time I had to spend on this project. 