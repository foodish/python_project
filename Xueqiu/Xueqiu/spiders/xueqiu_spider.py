from scrapy.http import Request
from Xueqiu.items import XueqiuItem
import scrapy


class Spider(scrapy.Spider):

    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Cookie': 'xq_a_token=720138cf03fb8f84ecc90aab8d619a00dda68f65'
    }
    base_url = 'https://xueqiu.com/friendships/groups/members.json?uid=1955602780&gid=0&page='

    def start_requests(self):
        for i in range(1, 661):
            url = self.base_url + str(i)
            yield Request(url, self.parse, headers=self.headers )


    def parse(self, response):
        print(response.text)
