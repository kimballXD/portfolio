
# coding: utf-8
#%% 1.set up
import os
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import jieba.analyse as jiebaa
from wordcloud import WordCloud

# read files
os.chdir('C:\\Coding\\zhnlp\\dpp_tv\\')

with open('data\\tsai.txt','r', encoding='utf8') as infile:
    tsai = infile.read()
    
with open('data\\lai.txt','r', encoding='utf8') as infile:
    lai = infile.read()    


#%% 2. 關鍵字抽取與解釋 Keyword extraction and Interpretation
    
## take a look on dictionary: pd.Series(jieba.dt.FREQ)
## correct frequency
jieba.add_word('民進黨',20)
jieba.add_word('前院長',20)

# keyword extraction (by textrank alogirhtm in jieba)
tsai_key = jiebaa.textrank(tsai, 50, withWeight=True, withFlag=True)
tsai_key = [('tsai', idx, item[0].word ,item[1], item[0].flag) for idx, item in enumerate(tsai_key)]
lai_key = jiebaa.textrank(lai, 50, withWeight=True, withFlag=True)    
lai_key = [('lai', idx, item[0].word ,item[1], item[0].flag) for idx, item in enumerate(lai_key)]    


# keywords DataFrame
tsai_df = pd.DataFrame(tsai_key, columns=['candidate','rank','word','textrank','pos'])
tsai_df.head()
lai_df = pd.DataFrame(lai_key, columns=['candidate','rank','word','textrank','pos'])
lai_df.head()


#%% 3. 關鍵字文字雲 Text is cheap. Show me the graph (word cloud)

# word cloud generation function 
def get_wordcloud(d, title, **kwargs):
    cloud = WordCloud(**kwargs)
    g = cloud.generate_from_frequencies(d)

    plt.imshow(g) 
    plt.title(title, size=18)
    plt.axis("off") 
    plt.tight_layout(pad = 0)  
    plt.show() 

# graph setting 
import matplotlib.font_manager as fm
name = plt.rcParams['font.sans-serif'][0]
fname = [f.fname for f in fm.fontManager.ttflist if f.name==name][0]
wc_param = {'width':800, 'height':600, 'background_color':'white', 'font_path':fname}    
plt.rcParams['figure.figsize']=[8,6]


# draw graph
get_wordcloud(dict(zip(tsai_df.word, tsai_df.textrank)), "蔡英文文字雲 Tsai's Word Cloud", **wc_param)
get_wordcloud(dict(zip(lai_df.word, lai_df.textrank)), "賴清德文字雲 Lai's Word Cloud", **wc_param)

