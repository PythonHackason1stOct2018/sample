# -*- coding: utf-8 -*-
import scrapy
import re


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["npb.jp"]
    start_urls = [
        'http://npb.jp/games/2018/schedule_03_detail.html',
    ]

    def parse(self, response):
        for url in response.css("a ::attr(href)").extract():
            if re.match(u'/scores/2018/\\d+/\\w\\-\\w\\-\\d\\d/$', url) :
                yield scrapy.Request(response.urljoin(url), callback=self.parse_game_page)
            if re.match(u'.*/schedule_\\d+_detail.html', url) :
                yield scrapy.Request(response.urljoin(url), callback=self.parse)

    def parse_game_page(self, response):
        item = {}
        item["GameDay"] = response.css('.game_tit > time *::text').extract_first()
        item['VisitorTeam'] = response.css(
            '.line-score > div > table > .top > th > span *::text, .line-score > div > table > tbody > .top > th > span *::text'
        ).extract_first()
        item['VisitorScore'] = response.css(
            '.line-score > div > table > .top > .total-1 *::text, .line-score > div > table > tbody > .top > .total-1 *::text'
        ).extract_first()
        item['HomeTeam'] = response.css(
            '.line-score > div > table > .bottom > th > span *::text, .line-score > div > table > tbody > .bottom > th > span *::text'
        ).extract_first()
        item['HomeScore'] = response.css(
            '.line-score > div > table > .bottom > .total-1 *::text, .line-score > div > table > tbody > .bottom > .total-1 *::text'
        ).extract_first()
        yield item
