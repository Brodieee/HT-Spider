# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Wangyiyun3Pipeline(object):
    def __init__(self):
        self.f = open('wyy3.csv', 'a', encoding='utf-8')
        self. f.write('music_id,music_name,singer,comment_num' + '\n')

    def process_item(self, item, spider):
        self.f.write(str(item['music_id']) + ',' + str(item['music_name']) + ',' + str(
            item['singer']) + ',' + str(item['comment_num']) + '\n')
        return item

    def close_spider(self,spider):
        self.f.close()


class Wangyiyun3MySQLPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',  # 使用自己的用户名
            passwd='ht19970910',  # 使用自己的密码
            db='wangyiyun',  # 数据库名
            charset='utf8')
        self.cursor = self.client.cursor()

    def process_item(self,item,spider):
        sql = 'insert into wangyiyun(music_id,music_name,singer,comment_num) values (%s,%s,%s,%s)'
        lis = (item['music_id'], item['music_name'], item['singer'], item['comment_num'])
        self.cursor.execute(sql, lis)
        self.client.commit()

        return item

    def close_item(self):
        self.cursor.close()
        self.client.close()