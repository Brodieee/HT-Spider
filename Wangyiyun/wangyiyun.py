from selenium import webdriver
import time
import json
import random
import base64
import binascii

from Crypto.Cipher import AES


# class Wangyiyun(object):
#
#     def __init__(self):
#         self.first_param = '{"rid":"R_SO_4_1413585838","offset":"0","total":"true","limit":"20","csrf_token":""}'
#         self.second_param = '010001'
#         self.third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
#         self.fourth_param = '0CoJUm6Qyw8W8jud'
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#             'Cookie': 'mail_psc_fingerprint=ea3e8a925d05d58443320b2ac14635f1; _iuqxldmzr_=32; _ntes_nnid=14a04e88138548c8aceb5a621e8f2052,1569220695055; _ntes_nuid=14a04e88138548c8aceb5a621e8f2052; WM_TID=uD7Xy8tFW79BQFBAFAY5t2Ox9j4aPCUx; P_INFO=yuren_ht333@163.com|1582962287|0|other|00&99|null&null&null#jix&null#10#0#0|182910&1|urs|yuren_ht333@163.com; WM_NI=TVX7NbXYk7nQ6wFhiWKbmSJOIFFtrQTY0nz%2BggxwRucl1YyPunpAlwzyBymDjwYcjyWmT4r4QTiozXJGrVwm5c%2FX8LrX%2F%2BtEHLoh36PqhZBaz09%2B%2FOZRr7JmUEvgICGkUzE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed2ae43ed8eae91b652f1968ba3d55a928a8abbf44af4929fccfc43bced8bd1e82af0fea7c3b92a988a98d8cd6a9c87a5d8ed5bf6a98a89ec5d89bea3b4c9458b9a8a95f15b9887008ff921a5b9b898d17fa1b4ffbafc5cb7b2c0a2ef7dbaa78e9af050aaa99784e97395b39cd5f140938ca790f9548a99beb7f667f7bde1b9bb48b288e1ccf74f8c94a189b23e94afa8bbc16bbaf0f7ccae459a8ebed8c967979bba88cc4985b59b9bc837e2a3; __51cke__=; __tins__19988117=%7B%22sid%22%3A%201585130217030%2C%20%22vd%22%3A%205%2C%20%22expires%22%3A%201585132926052%7D; __51laig__=7; JSESSIONID-WYYY=32hQH4o1NmBPJl4Stc%2BzVexT1M%2B3wYHmYE9MhS8%2F%5Ch%5CoFSW%2FACY1AGZ%5Cvb0uVMY0ghd%2FJYh1sXN%2FX7dWk%5CTbJkvEbxNDMWGQK3kAPrPk2epej4JcmZ%5CWWxmgw73WkqY5OTYQFa60Mbx%5CYJU1UmuTwfYbZo0uvGvio6CB97ypakmvh0bm%3A1585147041633'
#             }
#
#     def get_random_str(self):
#         """随机生成16位字符串"""
#         string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#         result = ''
#         for i in range(16):
#             index = random.randint(0,len(string)-1)
#             result += string[index]
#         return result
#
#     def aes_encrypt(self,text,key):
#         """
#         AES加密
#         text:加密内容
#         key:加密key
#         """
#         iv = b'0102030405060708'
#         pad = 16 - len(text) % 16
#         text = text + pad * chr(pad)
#
#         encryptor = AES.new(key.encode(), AES.MODE_CBC, iv)
#         encryptor_str = encryptor.encrypt(text.encode('utf-8'))
#         result_str = base64.b64encode(encryptor_str).decode('utf-8')
#         return result_str
#
#     def rsa_encrypt(self, pubkey, text, modules):
#         """
#         AES加密
#         :param pubkey:
#         :param text:
#         :param modules:
#         :return:
#         """
#         reversed_text = text[::-1]
#         result = pow(int(binascii.hexlify(reversed_text.encode()), 16), int(pubkey, 16), int(modules, 16))
#         return format(result, 'x').zfill(131)
#
#     def get_params(self):
#         i = random_str
#         encText = self.aes_encrypt(self.first_param, self.fourth_param)
#         encText = self.aes_encrypt(encText, i)
#         encSecKey = self.rsa_encrypt(self.second_param, i, self.third_param)
#         return {
#             "encText": encText,
#             "encSecKey": encSecKey
#         }
#
#
#
#
# if __name__ == '__main__':
#     wyy = Wangyiyun()
#     random_str = wyy.get_random_str()




class Wangyiyun(object):

    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def get_content(self):
        self.driver.get(self.url)
        self.driver.switch_to.frame(0)
        for x in range(51):
            js = 'window.scrollBy(0,8000)'
            self.driver.execute_script(js)
            time.sleep(3)
            elements = self.driver.find_elements_by_xpath('//div[@class="itm"]')
            for element in elements:
                result = element.find_element_by_xpath('.//div[@class="cnt f-brk"]').text
                # result = result.split(':')[1]
                # print(result)
                # print(result.split('：')[1:])
                content = ''.join(result.split('：')[1:])
                print(content)
                self.save(content)
            self.driver.find_element_by_partial_link_text('下一').click()
            time.sleep(3)

    def save(self,content):
        with open('wyy.txt','a',encoding='utf-8') as f:
            f.write(content + '\n')

if __name__ == '__main__':
    url = 'https://music.163.com/#/song?id=85580'
    wangyiyun = Wangyiyun(url)
    wangyiyun.get_content()
