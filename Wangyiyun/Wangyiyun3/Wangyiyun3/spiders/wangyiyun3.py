# -*- coding: utf-8 -*-
import scrapy
import re

class Wangyiyun3Spider(scrapy.Spider):
    name = 'wangyiyun3'
    allowed_domains = ['163.com']
    start_urls = [f'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={page*35}' for page in range(38)]

    def parse(self, response):
        selectors = response.xpath('//*[@id="m-pl-container"]/li/div[1]/a/@href').getall()
        for selector in selectors:
            playlist_url = 'https://music.163.com' + selector
            yield scrapy.Request(playlist_url, callback=self.parse_playlist)

    def parse_playlist(self, response):
        music_hrefs = response.xpath('//ul[@class="f-hide"]/li/a/@href').getall()
        for music_href in music_hrefs:
            music_id = ''.join(re.findall(r'id=(\d+)$', music_href))
            music_url = 'https://music.163.com' + music_href
            comment_url = f'http://music.163.com/api/v1/resource/comments/R_SO_4_{music_id}?limit=20&offset=0'
            yield scrapy.Request(comment_url, callback=self.parse_comment, meta={'music_id':music_id, 'music_url':music_url})

    def parse_comment(self, response):
        music_id = response.meta['music_id']
        music_url = response.meta['music_url']
        comment_num = re.findall(r'"total":(\d+)', response.text)[0]
        yield scrapy.Request(music_url, callback=self.parse_music, meta={'music_id':music_id, 'comment_num':comment_num})

    def parse_music(self, response):
        music_id = response.meta['music_id']
        comment_num = response.meta['comment_num']
        music_name = re.findall(r'data-res-name="(.*?)"',response.text)[0]
        singer = re.findall(r'data-res-author="(.*?)"',response.text)[0]
        item = {
            "music_id": music_id,
            "music_name": music_name,
            "singer": singer,
            "comment_num": comment_num
        }
        print(item)
        yield item