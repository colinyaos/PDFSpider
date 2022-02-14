# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import requests

class PdfSpiderPipeline:
    def process_item(self, item, spider):
        item_url = item[2:]

        r = requests.get(item_url, stream = True)

        with open("test.pdf","wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                # writing one chunk at a time to pdf file
                if chunk:
                    pdf.write(chunk)

        return item
