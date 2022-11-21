#Scripts\activate เพื่อเข้าไปใน environment 
#ก่อนใช้ ให้เข้าไปใน tutorial ก่อน โดยการ cd week03
#ใช้ scrapy crawl quotes -o LMAOXD.csv โดย LMAOXD คือชื่อไฟล์ และ .csv คือนามสกุลที่อยากได้ สามารถเปลี่ยนเป็น json ได้
#ใช้ scrapy shell https://store.steampowered.com/app/551170/Onmyoji/ เพื่อ test
#Tutorial Vid : https://youtu.be/ALizgnSFTwQ

import scrapy
import time
import random
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://store.steampowered.com/app/2089350/Hatsune_Miku_Logic_Paint_S/'

        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=1
            )

    def parse(self, response):
        for quote in response.css('div.page_content_ctn'):
            yield {
                'url' : response.request.url,
                'title': quote.css('.apphub_AppName::text').get(),
                'tag': quote.css('.app_tag::text').re('Hero Shooter|Battle Royale|Competitive|Roguelite|JRPG|Story Rich|Automobile Sim|Sports|Racing|Driving|Immersive Sim|Tactical|Management|Third Person|Simulation|Co-op|Local Multiplayer|Online Co-Op|PvE|Football|Soccer|PvP|Controller|Team-Based|Realistic|Local Co-Op|Multiplayer|Singleplayer|Anime|Strategy|Card Battler|Casual|PvP|Turn-Based Tactics|Card Game|Deckbuilding|Comic Book|Free to Play|Early Access|Superhero|Stylized|RPG|Free to Play|Turn-Based|Adventure|Fantasy|Stealth|Horror|Action|Parody|Retro|Funny|FPS|Shooter|Open World'),
                #([A-Z])\w+')
                # 'price' : quote.css('.game_purchase_price.price::text').get(),
                # 'price02' : quote.css('.game_purchase_price.price::text').getall(),
                'price' : quote.css('.game_purchase_price.price::text').re('Free To Play|Free|\d+'),
                'discounted price' : quote.css('.discount_original_price::text').get()
            } 
        
        next_page = response.css('div.store_horizontal_autoslider_ctn a::attr(href)').get()
        next_pages = response.css('div.block_responsive_horizontal_scroll a::attr(href)').getall()
        for next_page in next_pages:
            if next_page is not None:
                #time.sleep(5)
                next_page = response.urljoin(next_page)
                yield SeleniumRequest(url=next_page, callback=self.parse,wait_time=1)

            