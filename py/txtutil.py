# 텍스트를 줄단위로 끊어서 불러온뒤
# Token 단위로, 한글명사들을 추출한다
def txtnoun(filename , skip=False):

    try:
        # konlpy 0.4.4 이하인 경우
        from konlpy.tag import Twitter
        twitter   = Twitter()
    except:
        # konlpy 0.4.5 이상인 경우
        from konlpy.tag import Okt
        twitter   = Okt()

    import re

    with open(filename, 'r', encoding='utf-8') as f:
        contents = f.readlines()

    result = []
    for content in contents:
        texts     = content.replace('\n', ' ') # 해당줄의 줄바꿈 내용 제거
        tokenizer = re.compile(r'[^ ㄱ-힣]+')  # 한글과 띄어쓰기를 제외한 모든 글자를 선택
        tokens    = tokenizer.sub('', texts)   # 한글과 띄어쓰기를 제외한 모든 부분을 제거
        tokens    = tokens.split(' ')
        sentence  = []

        for token in tokens:
            # skip 대상이 없을 떄
            if skip == False:
                temp = twitter.nouns(token)
                if len("".join(temp)) > 1:
                    sentence.append("".join(temp))

            # skip 내용이 있을 때
            else:
                if token in skip:
                    result.append(token)
                else:
                    temp = twitter.nouns(token)
                    if len("".join(temp)) > 1:
                        sentence.append("".join(temp))

        # 단락별 작업이 끝난 뒤 '\n'를 덧붙여서 작업을 종료
        temp = "".join(sentence)
        if len(temp) < 2:
            pass
        else:
            sentence = " ".join(sentence)
            sentence += "\n"
            result.append(sentence)

    return " ".join(result)



# tf-idf 데이터 값들을 Rank 값으로 변환
def table_rank(series):
    rank, result  = {}, {}
    # 순번 데이터 추출하기
    set_values = list(set(series.values))
    set_values.sort(reverse=False)
    for no, i in enumerate(set_values):
        rank[i] = no + 1
    # 원본 데이터에 순번을 적용
    for k, v in series.items():
        result[k] = rank[v]
    import pandas as pd
    result = pd.Series(result)
    return result.sort_values(ascending=False)


# https://gist.github.com/himzzz/4105717
# tf-idf 사용자 함수
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math

# 단어별 빈도수 계산
def freq(word, doc):
    return doc.count(word)

def word_count(doc):
    return len(doc)

def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))

def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count

def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
            float(num_docs_containing(word, list_of_docs)))

# doc : 가운데가 많아질수록 tfidf값이 커진다
# doc : 분석대상 Text
# list_of_docs : 분석 기준이 되는 token들의 모음
def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))