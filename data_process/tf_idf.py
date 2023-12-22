from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
import re
import jieba.analyse


def participle(sentence):
    stopwords = [line.strip() for line in open("cn_stopwords.txt", encoding='UTF-8').readlines()]
    for j in range(len(sentence)):
        sentence[j] = re.sub(r"</?(.+?)>|&nbsp;|\t|\r", "", sentence[j])
        sentence[j] = re.sub(r"\n", "", sentence[j])
        sentence[j] = re.sub('[a-zA-Z0-9]', "", sentence[j])
        sentence[j] = re.sub(
            "[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]"
            , "", sentence[j])
#         seg = jieba.lcut(sentence[j], cut_all=False)
#         print(sentence[j])
        seg = jieba.analyse.textrank(sentence[j], topK=None, withWeight=False, allowPOS=('ns', 'n', 'vn', 'nt', 'nz'), withFlag=False)
        sentence[j] = ''
        for word in seg:
            if word not in stopwords:
                sentence[j] = sentence[j] + word + " "

    for _ in range(sentence.count("")):
        sentence.remove("")
    return sentence


def tfidf(sentence):
    words = []
    # step 1
    vectoerizer = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
    # step 2
    vectoerizer.fit(sentence)
    # step 3
    bag_of_words = vectoerizer.get_feature_names_out()
    # step 4
    X = vectoerizer.transform(sentence)

    # step 1
    tfidf_transformer = TfidfTransformer()
    # step 2
    tfidf_transformer.fit(X.toarray())
    # step 3
    for idx, word in enumerate(vectoerizer.get_feature_names_out()):
        words.append((word, tfidf_transformer.idf_[idx]))
    # step 4
    # tfidf = tfidf_transformer.transform(X)
    # print(tfidf.toarray())

    words.sort(key=lambda word: word[1], reverse=True)
    words = [i[0] for i in words]

    return words
