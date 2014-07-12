# Scrapy settings for cne project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os


BOT_NAME = 'cne'

SPIDER_MODULES = ['cne.spiders']
NEWSPIDER_MODULE = 'cne.spiders'

CONCURRENT_ITEMS = 200
CONCURRENT_REQUESTS = 50
DOWNLOAD_DELAY = 0.01

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:26.0) Gecko/20100101 Firefox/26.0'

ITEM_PIPELINES = {
    'cne.pipelines.FormatDataPipeline': 200,
}

INSTALL_ROOT = os.path.dirname(os.path.abspath(__file__))

AGGREGATE_DB_CONF = { 
    'db': os.environ.get('CNE_DB_NAME', 'scrapy'),
    'user': os.environ.get('CNE_DB_USER', 'scrapy'),
    'password': os.environ.get('CNE_DB_PASSWORD', 'scrapy'),
    'host': os.environ.get('CNE_DB_HOST', 'localhost'),
    'port': os.environ.get('CNE_DB_PORT', 3306)
}

AGGREGATE_DB = create_engine(
    'postgresql+psycopg2://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % AGGREGATE_DB_CONF, 
    echo=False,
    encoding='utf-8',
    convert_unicode=True,
)

AGGREGATION_ENABLED = True
