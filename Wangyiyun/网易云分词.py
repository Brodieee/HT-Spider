import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

inputs = open('wyy.txt', 'r', encoding='utf-8')
lines = ''
for line in inputs:
    lines += line.replace("\n", "")
inputs.close()
words = jieba.cut(lines)
content = ''
for word in words:
    if len(word)>1 and word != '\r\n':
        content = content + ' ' + word
print(content)
mask = np.array(Image.open('F:\Data analysis\wordcloud\huanglei.png'))
wc = WordCloud(background_color='white',repeat=True,max_words=300,mask=mask,
                     max_font_size=200,min_font_size=20,font_path='fonts/msyh.ttc',width=1200,height=800).generate(content)
plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()