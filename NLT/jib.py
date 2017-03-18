import jieba


s = jieba.cut('我们是中国最大的云服务提供商', cut_all=True)
s_split = ' '.join(s) # 引号中间要有空格，不然分开的词又连到一起
print('全模式：', s_split)

s = jieba.cut('我们是中国最大的云服务提供商', cut_all=False)
s_split = ' '.join(s) # 引号中间要有空格，不然分开的词又连到一起
print('精确模式：', s_split)

s = jieba.cut('''巴萨末轮5比2屠杀塞维利亚，拉科则0比0战平瓦伦西亚，巴萨最终在积分相同的情况下靠直接交锋时的战绩优势夺冠。
神奇的是，拉科球员久基奇在终场前踢丢点球，这才有了巴萨的逆袭。''')  # 默认为精确模式
s_split = ' '.join(s)
print('新词识别（默认精确模式）：', s_split)

s = jieba.cut_for_search('''巴萨末轮5比2屠杀塞维利亚，拉科则0比0战平瓦伦西亚，巴萨最终在积分相同的情况下靠直接交锋时的战绩优势夺冠。
神奇的是，拉科球员久基奇在终场前踢丢点球，这才有了巴萨的逆袭。''')  # 搜索引擎模式
s_split = ' '.join(s)
print('搜索引擎模式：', s_split)