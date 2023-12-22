import sys
import json
import time
import requests
# skip https auth
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode


class Emotion:
    """
    传入参数说明：
            生成对象时需传入KEY和SECRET
            预测时传入文本内容

    返回参数说明：
            若正常取得预测结果则返回：
                情感极性分类结果    int     0:负向，1:中性，2:正向
                positive_prob	float	表示属于积极类别的概率 ，取值范围[0,1]
                negative_prob	float	表示属于消极类别的概率，取值范围[0,1]
    """
    def __init__(self, key, secret):
        self.API_KEY = key
        self.SECRET_KEY = secret
        self.COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
        self.TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

    def fetch_token(self):
        global result_str
        params = {'grant_type': 'client_credentials',
                  'client_id': self.API_KEY,
                  'client_secret': self.SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(self.TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print(err)
        if IS_PY3:
            result_str = result_str.decode()

        result = json.loads(result_str)

        if 'access_token' in result.keys() and 'scope' in result.keys():
            if 'brain_all_scope' not in result['scope'].split(' '):
                print('please ensure has check the  ability')
                exit()
            return result['access_token']
        else:
            print('please overwrite the correct API_KEY and SECRET_KEY')
            exit()

    def make_request(self, comment):

        token = self.fetch_token()
        url = self.COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token
        comment = {"text": comment}

        print("---------------------------------------------------")
        # print("    ", comment)

        response = requests.post(url, json.dumps(comment))

        data = json.loads(response.text)

        print(data)

        # 防止qps超限
        time.sleep(0.05)
        if "items" not in data.keys():
            return "null", "null", "null"
        else:
            return data["items"][0]["sentiment"], data["items"][0]["positive_prob"], \
                   data["items"][0]["negative_prob"]
