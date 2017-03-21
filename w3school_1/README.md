采用scrapy框架 和 xpath语法

##遇到的坑

1.xpath语法中属性值应双引号而非单引号; a/text()而非a.text()

2.spider not found error:运行时的entrypoint中的爬虫名字应与spider.py中设置的name字段
一致.

##reference

http://blog.csdn.net/u012150179/article/details/32911511
