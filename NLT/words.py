import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba


text = open('1.txt', encoding='utf-8').read()

wordlist_jieba = jieba.cut(text, cut_all = True)
wl_space_split = ''.join([i for i in wordlist_jieba])
#wl_space_split = ''.join(wordlist_jieba)  # 后面报错：IndexError: list index out of range

my_wordcloud = WordCloud().generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis('off')
plt.show()