# 破解科大研究生网络课堂视频

import requests
from bs4 import BeautifulSoup

link = 'http://wlkt.ustc.edu.cn/video/detail_2792_0.htm' #网络课堂单个视频的播放
req = requests.get(link)
# print(req)
# req = req.text
req = req.content
# print(req)
soup = BeautifulSoup(req, 'lxml')
result = soup.find_all('div')
print(result)
# url = 'http://wlkt.ustc.edu.cn/ajaxprocess.php?hid_video_type=flv&file='+ result
# print('真实下载地址是：' + url)

"""
# http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=YOXUM2UJI3MVRM02GR98KFD6O9NBDHKT  #插件嗅探的地址
http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=0P12YP7JET1ZCRLP2I9YEXIR62FM924S&start=2452169 #插件嗅探的地址
http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=0P12YP7JET1ZCRLP2I9YEXIR62FM924S #插件嗅探的地址
http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=laodii12iakdW7ZJ6AICDX30441TYCJSPBQAKF2Y50NWapoi112dkia
http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=W7ZJ6AICDX30441TYCJSPBQAKF2Y50NW%20/jita_1.flv#直接放入地址栏不可以
http://wlkt.ustc.edu.cn/video_stream.php?hid_video_type=flv&file=W7ZJ6AICDX30441TYCJSPBQAKF2Y50NW%20 #后面的去掉放入地址栏按回车后自动添加，然后下载
http://wlkt.ustc.edu.cn/video_stream.php?file=W7ZJ6AICDX30441TYCJSPBQAKF2Y50NW /jita_1.flv
<input type="hidden" name="videourl" id="videourl" value="http://mooc.ustc.edu.cn/wlkt/video_stream.php?file=laodii12iakdW7ZJ6AICDX30441TYCJSPBQAKF2Y50NWapoi112dkia" />
<!--    /video_stream.php?file=W7ZJ6AICDX30441TYCJSPBQAKF2Y50NW /jita_1.flv-->




"""