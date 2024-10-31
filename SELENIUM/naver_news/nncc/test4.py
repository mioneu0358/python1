# -*- coding: utf-8 -*-
import pandas as pd
import datetime

# 엑셀 저장하기
now = datetime.datetime.now()
excelfilename = f"{now.year}_{now.month}_{now.day}_킥보드.xlsx"

loadExcel = pd.read_excel(excelfilename)
print(loadExcel)


from konlpy.tag import Okt
okt = Okt()         # 형태소 분석기
nouns_comments = []

for commentList in list(loadExcel['comments']):
    comments = commentList.split('\n')
    nounsList = []
    for comment in comments:
        nouns = okt.nouns(comment)  # 명사만 추출
        nounsList.append(nouns)
    nouns_comments.append(nounsList)
print(nouns_comments)

# 댓글들에서 명사들만 분리한 값들을 저장한 리스트
nouns_comments = [[['판쇠', '변호', '술', '한잔'], ['파면', '면'], ['이', '몇', '기사', '쏱', '슈가', '혼자', '술', '기사', '욕']],
                  [['교통', '수단', '륜', '베트남', '필리핀', '등'], ['과연', '필리핀', '국민성']]]

all_nouns = ''
for comments in nouns_comments:
    for comment in comments:
        all_nouns += ' '.join(comment)+ ' '     # '판쇠 변호 술 한잔' + ' ', ....
print(all_nouns)

from wordcloud import WordCloud

# # 가장 기본 적인 워드클라우드 생성
fontPath = "C:\Windows\Fonts\malgun.ttf"
wdcd = WordCloud(font_path=fontPath).generate(all_nouns)
print(wdcd)
print(type(wdcd))        # 자료형이 wordcloud이기 때문에 우리가 잘 아는 자료형으로 변경한다.
words = wdcd.words_      # words_: dict로 변환한 값을 돌려주는 메서드, 이 메서드를 사용하는 이유는 딕셔너리로 바로 변환이 불가능하기 때문
print(words)
print(type(words))

# 단어 개수 제한
# wdcd = WordCloud(font_path=fontPath, max_words=100).generate(all_nouns)

STOPWORDS = set()
STOPWORDS.add('불용어')
# wdcd = WordCloud(font_path=fontPath,background_color='white', stopwords=STOPWORDS).generate(all_nouns)

from PIL import Image
import numpy as np
alice_mask = np.array(Image.open('C:\\Users\\turing11\\PycharmProjectFolder\\pythonProject38\\bc.png'))
print(alice_mask)
#
wdcd = WordCloud(font_path=fontPath,mask = alice_mask,background_color='white', stopwords=STOPWORDS).generate(all_nouns)

import matplotlib.pyplot as plt

plt.figure(figsize=(15,10))
plt.imshow(wdcd)
plt.axis("off")                         # 불필요한 축 제거
plt.show()                              # 결과 확인용
plt.savefig('wordcloud_commets.png')    # 만든 이미지 저장
