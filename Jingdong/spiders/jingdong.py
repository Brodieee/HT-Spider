# -*- coding: utf-8 -*-
import scrapy
import json
import re

class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    start_urls = [f'https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page={page}&s=56&click=0' for page in range(1,100)]

    def parse(self, response):

        # 数据提取
        selectors = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for selector in selectors:
            price = selector.xpath('.//div[@class="p-price"]//i/text()').get()
            title = selector.xpath('.//div[contains(@class,"p-name")]//em//text()').getall()
            productId = selector.xpath('./@data-sku').get()
            item = {
                'price': price,
                'title': ''.join(title),
                'productId': productId
            }
            print(item)
            # comments_list = []
            # 评论信息
            comments_url = f'https://sclub.jd.com/comment/productPageComments.action?productId={productId}&score=0&sortType=5&page=0&pageSize=10'
            yield item
            yield scrapy.Request(comments_url, meta={'productId': productId}, callback=self.parseComment)

    def parseComment(self, response):
        # 得到上一个方法中的数据
        # comments_list = response.meta.get('comments_list')
        productId = response.meta.get('productId')
        # 提取评论信息
        json_data = json.loads(response.text)

        maxPage = json_data.get('maxPage')

        if json_data.get('comments'):
            for dat in json_data['comments']:
                content = dat.get('content')
                print(content)
                # comments_list.append(content)

                items = {
                    # 'items': comments_list,
                    'content': content,
                    #'maxPage': maxPage,
                    'productId': productId
                }
                print(items)
                yield items

        # 翻页
        if json_data.get('maxPage'):
            maxPage = int(json_data['maxPage'])
            if maxPage>=2:
                for page in range(1, maxPage):
                    maxPageUrl = re.sub('page=\d+', f'page={page}', response.url)
                    # print(maxPageUrl)
                    yield scrapy.Request(maxPageUrl, callback=self.parseComment, meta={'productId': productId})
            
