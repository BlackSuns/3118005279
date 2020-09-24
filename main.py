import re # 正则包
import jieba
import jieba.analyse # 自然语言处理包
import html # html 包
from sys import argv

class JaccardSimilarity(object):
    # jaccard相似度
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content) # 正则过滤 html 标签
        content = html.unescape(content) # html 转义符实体化
        seg = [i for i in jieba.cut(content, cut_all=True) if i != ''] # 切割
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)  # 提取关键词
        return keywords

    def main(self):
        jieba.analyse.set_stop_words('stopwords.txt') # 去除停用词
        keywords_x = self.extract_keyword(self.s1) 
        keywords_y = self.extract_keyword(self.s2) # 分词与关键词提取
       
        intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
        union = len(list(set(keywords_x).union(set(keywords_y)))) # jaccard相似度计算
        sim = float(intersection)/union if union != 0 else 0 # 除零处理
        return sim


def openfile(argv):
    '''
    打开文件对比操作
    '''
    f = open(argv[1],'r',encoding='utf-8')
    g = open(argv[2],'r',encoding='utf-8')
    answer = open(argv[3],'a+',encoding='utf-8')
    f1 = f.read()
    g1 = g.read()
    similarity = JaccardSimilarity(f1, g1)
    similarity = similarity.main()
    strings = f'{argv[1]}和{argv[2]}相似度: %.2f%%' % (similarity*100)+"\n"
    answer.writelines(strings)
    print(strings)   
    f.close()
    g.close()
    answer.close()


if __name__ == '__main__':
    
    openfile(argv)

