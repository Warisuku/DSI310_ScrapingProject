import pandas as pd

df = pd.read_json (r'D:\Maxus\Thammasat University\DSI310\Week03 - Scrapy Selenium\dsi310week03\week03\lazada55.json')
df.to_csv (r'D:\Maxus\Thammasat University\DSI310\Week03 - Scrapy Selenium\dsi310week03\week03\lazada55.csv', index = None)