import sys
import json
import time
import requests
import copy
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


class Topic:
    """
    传入参数说明：
            生成对象时需传入KEY和SECRET
            预测时传入文本内容

    返回参数说明：
            若正常取得预测结果则返回：
                文本主题分类结果
                prob表示属于相应类别的概率
    """
    def __init__(self, key, secret):
        self.API_KEY = key
        self.SECRET_KEY = secret
        self.COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/topic"
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
        content = {
            "title": comment if len(comment) <= 40 else comment[:40],
            "content": comment if len(comment) <= 65535 // 2 else comment[:65535 // 2]
        }

        print("---------------------------------------------------")
        # print("    ", comment)

        response = requests.post(url, json.dumps(content))

        data = json.loads(response.text)

        print(data)

        # 防止qps超限
        time.sleep(0.05)

        if 'item' not in data.keys():
            return "null", "null"
        else:
            text_topic = data["item"]["lv1_tag_list"][0]["tag"]
            if text_topic in ["社会", "动漫", "汽车", "星座运势", "游戏", "搞笑", "旅游", "时事", "财经", "宠物", "综合"]:
                text_topic = "社会时事"
            elif text_topic in ["音乐", "娱乐", "体育"]:
                text_topic = "娱乐"
            elif text_topic in ["时尚", "美食", "健康养生", "家居"]:
                text_topic = "常识"
            elif text_topic in ["历史", "文化"]:
                text_topic = "历史文化"
            return text_topic, data["item"]["lv1_tag_list"][0]["score"]
