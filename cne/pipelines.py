# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class FormatDataPipeline(object):
    def process_item(self, item, spider):
        for key in item.keys():
            value = item[key]
            try:
                value = int(value)
            except ValueError:
                value.strip()
                value.lower()
            finally:
                item[key] = value
        return item
