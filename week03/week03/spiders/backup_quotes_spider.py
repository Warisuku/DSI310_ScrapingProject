#Scripts\activate เพื่อเข้าไปใน environment 
#ก่อนใช้ ให้เข้าไปใน tutorial ก่อน โดยการ cd week03
#ใช้ scrapy crawl quotes -o LMAOXD.csv โดย LMAOXD คือชื่อไฟล์ และ .csv คือนามสกุลที่อยากได้ สามารถเปลี่ยนเป็น json ได้
#ใช้ scrapy shell https://store.steampowered.com/app/551170/Onmyoji/ เพื่อ test
#Tutorial Vid : https://youtu.be/ALizgnSFTwQ

import scrapy
import time
import re
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class QuotesSpider(scrapy.Spider):
    name = 'quotes_backup'

    def start_requests(self):
        url = 'https://store.steampowered.com/app/1997040/MARVEL_SNAP/'
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=10
            )

    def parse(self, response):
        for quote in response.css('div.page_content_ctn'):
            yield {
                'url' : response.request.url,
                'title': quote.css('.apphub_AppName::text').get(),
                'tag': quote.css('.app_tag::text').re('Hero Shooter|Battle Royale|Competitive|Roguelite|JRPG|Story Rich|Automobile Sim|Sports|Racing|Driving|Immersive Sim|Tactical|Management|Third Person|Simulation|Co-op|Local Multiplayer|Online Co-Op|PvE|Football|Soccer|PvP|Controller|Team-Based|Realistic|Local Co-Op|Multiplayer|Singleplayer|Anime|Strategy|Card Battler|Casual|PvP|Turn-Based Tactics|Card Game|Deckbuilding|Comic Book|Free to Play|Early Access|Superhero|Stylized|RPG|Free to Play|Turn-Based|Adventure|Fantasy|Stealth|Horror|Action|Parody|Retro|Funny|FPS|Shooter|Open World'),
                #([A-Z])\w+')
                'price' : quote.css('.game_purchase_price.price').get(),
                'price.simp' : quote.css('.game_purchase_price.price::text').re('/Free To Play|\d+')
            } 
        
        #next_page = response.css('div.store_horizontal_autoslider_ctn a::attr(href)').get()
        # next_page = response.css('div.block_responsive_horizontal_scroll a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield SeleniumRequest(url=next_page, callback=self.parse)
