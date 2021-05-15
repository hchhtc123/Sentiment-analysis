import pandas as pd
from sklearn.utils import shuffle

# 读取数据集，数据的初始格式为label review
df = pd.read_csv('./simplifyweibo_4_moods.csv')

# 数据分析,数据的标签为0、1、2、3，根据标签进行对应
moods = {0: '喜悦', 1: '愤怒', 2: '厌恶', 3: '低落'}
print('微博数目（总体）：%d' % df.shape[0])
for label, mood in moods.items():
    print('微博数目（{}）：{}'.format(mood,  df[df.label==label].shape[0]))

# 做简单的交换，将评论文本review与标签label的位置进行交换变为review label的格式
mid = df['review']
df.drop(labels=['review'], axis=1,inplace = True)
df.insert(0, 'review', mid)
print('数据集总长度：', len(df))

# 替换数据集中标签,{0: '喜悦', 1: '愤怒', 2: '厌恶', 3: '低落'}
df.loc[df['label']==0, 'label'] = '喜悦'
df.loc[df['label']==1, 'label'] = '愤怒'
df.loc[df['label']==2, 'label'] = '厌恶'
df.loc[df['label']==3, 'label'] = '低落'

# 查看处理后的数据集前5行
print(df.head())

# 按类别进行8:1:1的训练、验证和测试集划分
train = pd.DataFrame()  # 剩余的train集合
test = pd.DataFrame()  # 划分出的test集合
valid = pd.DataFrame()  # 划分出的valid集合
tags = df['label'].unique().tolist()  # 按照该标签进行等比例抽取
# 根据数据集的类别按8:1:1的比例划分训练、验证和测试集并打乱后保存
for tag in tags:
        # 随机选取0.2的数据作为训练和验证集
        data = df[(df['label'] == tag)]
        sample = data.sample(int(0.2 * len(data)))
        sample_index = sample.index
        # 将剩余0.8的数据作为训练集
        all_index = data.index
        residue_index = all_index.difference(sample_index)  # 去除sample之后剩余的数据
        residue = data.loc[residue_index]  # 这里要使用.loc而非.iloc
        # 对划分出来的0.2的数据集按等比例进行测试集和验证集的划分
        test_sample = sample.sample(int(0.5 * len(sample)))
        test_sample_index = test_sample.index
        valid_sample_index = sample_index.difference(test_sample_index)  # 去除sample之后剩余的数据
        valid_sample = sample.loc[valid_sample_index]  # 这里要使用.loc而非.iloc
        # 保存
        test = pd.concat([test, test_sample], ignore_index=True)
        valid = pd.concat([valid, valid_sample], ignore_index=True)
        train = pd.concat([train, residue], ignore_index=True)
        # 对数据进行打乱
        train = shuffle(train)
        valid = shuffle(valid)
        test = shuffle(test)
# 保存为tab分隔的文本
test.to_csv('test.csv', sep='\t', index=False)
valid.to_csv('valid.csv', sep='\t', index=False)
train.to_csv('train.csv', sep='\t', index=False)
print('训练集长度：', len(train), '验证集长度：', len(valid), '测试集长度', len(test))