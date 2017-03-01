import requests
from bs4 import BeautifulSoup

url = 'https://www.zhihu.com/people/loveQt/answers'
headers = {
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  'authorization':'Bearer 2|1:0|10:1487570898|4:z_c0|76:QUFEQW04QVlBQUFtQUFBQVlBSlZUZElVMGxpaGFhVGxtazRUZmFoX3lFamlQN0I2YnNwYUlRPT0=|9a603ce132e67f9cb3cd427fbed284e39d1e3bcef461ed110a4f8e9900bdeb74'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
answers = soup.find_all('title')
answers = soup.find_all('a')
answers = soup.find_all('h1')
print(answers)
# print('用户名 %s' % author.name)
# print('用户简介 %s' % author.motto)
# print('用户关注人数 %d' % author.followee_num)
# print('取用户粉丝数 %d' % author.follower_num)
# print('用户得到赞同数 %d' % author.upvote_num)
# print('用户得到感谢数 %d' % author.thank_num)
# print('用户提问数 %d' % author.question_num)
# print('用户答题数 %d' % author.answer_num)

# print('用户专栏文章数 %d，名称分别为：' % author.post_num)

  # print(column.name)
# print('用户收藏夹数 %d，名称分别为：' % author.collection_num)
  # print(collection.name)