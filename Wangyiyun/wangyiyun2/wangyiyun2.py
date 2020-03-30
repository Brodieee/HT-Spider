import requests
import parsel
import re
import time
from threading import Thread


class Wangyiyun(object):
    def __init__(self):
        self.headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
        }

    def get_playlist(self,url):
        response = requests.get(url=url,headers=self.headers)
        # print(response.text)
        selector = parsel.Selector(response.text)
        playlists = selector.xpath('//*[@id="m-pl-container"]/li/div[1]/a/@href').getall()
        # print(playlists)
        self.get_song(playlists)

    def get_song(self, playlists):
        data = {}
        for playlist in playlists:
            playlist_url = 'https://music.163.com' + playlist
            # print(playlist_url)
            playlist_response = requests.get(url=playlist_url, headers=self.headers)
            # print(playlist_response.text)
            playlist_selector = parsel.Selector(playlist_response.text)
            music_hrefs = playlist_selector.xpath('//ul[@class="f-hide"]/li/a/@href').getall()
            # print(music_hrefs)
            self.get_song_info(music_hrefs,data)

    def get_song_info(self, music_hrefs, data):
        for music_href in music_hrefs:
            music_id = ''.join(re.findall(r'id=(\d+)$', music_href))
            comment_url = f'http://music.163.com/api/v1/resource/comments/R_SO_4_{music_id}?limit=20&offset=0'
            comment_response = requests.get(url=comment_url,headers=self.headers)
            comment_num = re.findall(r'"total":(\d+)', comment_response.text)[0]
            music_url = 'https://music.163.com' + music_href
            music_response = requests.get(url=music_url,headers=self.headers)
            # print(music_response.text)
            music_selector = parsel.Selector(music_response.text)
            music_name = music_selector.re('data-res-name="(.*?)"')[0]
            singer = music_selector.re('data-res-author="(.*?)"')[0]
            data['music_id'] = music_id
            data['music_name'] = music_name
            data['singer'] = singer
            data['comment_num'] = comment_num
            print(data)
            self.save_data(data)

    def save_data(self, data):
        with open('wyy2.csv', 'a', newline='', encoding='utf-8') as f:
            f.write(str(data['music_id']) + ',' + str(data['music_name']) + ',' + str(
                data['singer']) + ',' + str(data['comment_num']) + '\n')

    def run(self):
        with open('wyy2.csv', 'a', newline='', encoding='utf-8') as f:
            f.write('music_id,music_name,singer,comment_num' + '\n')
        start_time = time.time()
        for page in range(38):
            print(f"正在获取第{page+1}页歌单。。。。。。。")
            url = f'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={page*35}'
            self.get_playlist(url)
        end_time = time.time()
        print("耗时：", end_time - start_time)

if __name__ == '__main__':
    wangyiyun = Wangyiyun()
    wangyiyun.run()

