import pandas as pd
from scrapy import Selector
import requests 

#url, html, xpath 
url = "https://www.realtor.com/research/data/"
html = requests.get(url).text
xpath = "//table[@id = 'supsystic-table-12']//td[@data-cell-id = 'F3']/a/@href"

sel = Selector(text = html)
links = sel.xpath(xpath).extract()

#ingest data into pandas DF 
print("opening link: ")
print(links[0])
realtor_df = pd.read_csv(links[0])
print(realtor_df)