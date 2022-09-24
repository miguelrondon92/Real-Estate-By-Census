import pandas as pd
from scrapy import Selector
import requests

url = "https://www.realtor.com/research/data/"
html = requests.get(url).text
xpath = "//table[@id = 'supsystic-table-12']//td[@data-cell-id = 'F3']/a/@href"
dtype_dict = {
    'month_date_yyyymm': 'str',
    'postal_code': 'str',
    'zip_name':	'str',
    'median_listing_price': 'Int64',
    'active_listing_count': "Int64",
    'median_days_on_market': "Int64",
    'new_listing_count': "Int64",
    'price_increased_count': "Int64",
    'price_reduced_count': "Int64",
    'pending_listing_count': "Int64",
    'median_listing_price_per_square_foot': "Int64",
    'median_square_feet': 'Int64',
    'average_listing_price': "Int64",
    'total_listing_count': "Int64",
    'pending_ratio': 'Float64',
    'quality_flag': 'Int64'
}

df_keys = dtype_dict.keys()


#get csv file from website
sel = Selector(text=html)
links = sel.xpath(xpath).extract()

#ingest data into pandas DF
realtor_df = pd.read_csv(
    links[0], dtype=dtype_dict, skipfooter=1, usecols=list(df_keys))
