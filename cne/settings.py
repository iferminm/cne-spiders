# Scrapy settings for cne project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cne'

SPIDER_MODULES = ['cne.spiders']
NEWSPIDER_MODULE = 'cne.spiders'

CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 50
DOWNLOAD_DELAY = 0.01

#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:26.0) Gecko/20100101 Firefox/26.0'

ITEM_PIPELINES = {
    'cne.pipelines.FormatDataPipeline': 200,
}
