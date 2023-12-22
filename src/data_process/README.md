# Introducion of Class

## FILE: get_data.py
### Class: GetData
This class is used to get files from a database.
#### Parameter introduction

##### self.ori_data: list

> ```
> 每个元素也为一个list（长度为12），
> 存储：微博内容及相关信息（'_id', 'user_id', 'content', "comment_num", "like_num", "repost_num", "crawl_time",
> "created_at", "image_url", "video_url", "weibo_url", "origin_weibo"）
> 内容来源参考：Text2020.csv
> 示例：
> [
>     [
>     'InFnuqpW4',
>     1202586970,
>     '#毽客视线#一位河南省政府官员，在高速公路付费通道时拿错了银行卡，刷卡后当即被爆露卡上的巨大余额，一个星期后就被双规！😂 这时你就该
>     知道官员财产申报和公示为什么提出来这么多年却迟迟没有下文 ，因为不但干净的人太少了，而且一个赛一个能贪，真要通过了那不是革自己的命吗？
>     按说抓了那么多老虎，应该收敛一点才是，怎么还是层出不穷[抓狂]为什么…… 毽客逆风飞扬的微博视频',
>     '0', 0, '0', '1609906443', '2020-01-02 21:57:40    ', None, None,
>     'https://weibo.com/5150457067/InFnuqpW4', None
>     ]
>     ...
> ]
> ```

##### self.time: dict

> ```
> 键值为用户id，
> 值类型为str，
> 存储每条信息的发布时间，
> 示例：{"InzJsiQ1k"：'2020-01-02 07:35:18'
>         ...
>     }
> ```

##### self.influence: dict

> ```
> 键值为用户id，
> 值类型为dict，
> 存储转评赞信息，
> 示例：{"InzJsiQ1k":{
>                     'repost': '13',
>                     'comment': '43',
>                     'like': 53
>                 }
>     ...
>     }
> ```

##### self.user_info: dict

> ```
> 键值为用户id，
> 值类型为dict，
> 存储用户信息：'id', 'authentication','birthday','brief_introduction','city','fans_num',
>             'follows_num','gender','labels','province','sentiment','sex_orientation',
>             'tweets_num','vip_level'
> 内容来源参考：User2020.csv
> 示例：{1202586970:{
>                  'id': 1202586970,
>                  ’nick_name‘: ,
>                  'authentication': nan,
>                  'birthday': '2013-10-12',
>                  'brief_introduction': '一个还赖在尘世中的修行者，只因还有一份责任和使命感。',
>                  'city': nan,
>                  'fans_num': 222153,
>                  'follows_num': 19,
>                  'gender': '男',
>                  'labels': '自由,情感,个性',
>                  'province': '北京',
>                  'tweets_num': 4840,
>                  'vip_level': '6级'
>                  }
>          ...
>         }
> ```

##### self.forward_info:dict

> ```
> 键值为微博内容id，
> 值类型为list，存储参与转发的信息（长度为2，类型为str）
> 内容来源参考：Forwards2020.csv
> 示例：{"InzJsiQ1k":[
>                 ['7007025883', '大雄42193:'],
>                 ['6187132230', '美丽的和谐家园8868:'],
>                 ['6389479884', '用户蓝天彩虹6389479884:转发微博'],
>                 ['6006625578', '靠谱的钟爱一生585:[赞啊][求关注][好喜欢]'],
>                 ['5869967115', '一江春水落花流:它們可以如此的囂張， 全歸功於人們的縱容。'],
>                 ['1548434974', '手机用户4349749793_681:[偷笑]'],
>                 ['7161003036', '小蜜蜂哇哇叫:[哆啦A梦微笑][哆啦A梦吃惊]'],
>                 ['1109305345', '迷迷糊糊地转:这事是真的呀？'],
>                 ['5165089330', '樱淼的微博:应该把权力扼杀在摇篮！'],
>                 ['5450035157', '天蝎座的夏美:转发微博'],
>                 ['1409455782', '槐花几时开666:德国人创立/的学说没有在德国发展起来，却在亚洲大放异彩，几十年来培养了无数的捞钱人才。']
>                 ]
>        ...
>     }
> ```

##### self.forward_users_info: dict

> ```
> 键值为用户id，
> 值类型为dict，
> 存储用户信息：'id','authentication','birthday','brief_introduction','city','fans_num',
>             'follows_num','gender','labels','province','sentiment','sex_orientation',
>             'tweets_num','vip_level'，
> 内容参考来源:ForwardUsers2020.csv
> 示例：{"7007025883":{
>                     'id': '7007025883',
>                     ’nick_name‘: ,
>                     'authentication': nan,
>                     'birthday': nan,
>                     'brief_introduction': nan,
>                     'city': nan,
>                     'fans_num': 94.0,
>                     'follows_num': 203.0,
>                     'gender': '男',
>                     'labels': nan,
>                     'province': '其他',
>                     'tweets_num': 33346.0,
>                     'vip_level': '未开通'
>                     }
>        ...
>     }
> ```

##### self.emotion: dict

> ```
> 键值为微博内容id，
> 值类型为dict，
> 存储情感信息，'value', 'positive_prob', 'negative_prob'
> 内容参考来源：emotion.csv,
> 示例：{“DzIBEpf1T”:{
>                     "value":-1,
>                     "positive_prob":0.00275745,
>                     "negative_prob":0.997243
>                     }
>     ...
>     }
> ```

##### self.topic: dict

> ```
> 键值为微博内容id，
> 值类型为dict，
> 存储情感信息，'topic', 'prob',
> 内容参考来源：topic.csv,
> 示例：{“DzIBEpf1T”:{
>                     "topic":"社会时事",
>                     "prob":0.863377
>                     }
>     ...
>     }
> ```

##### self.commentusers: dict

> ```
> 键值为用户id，
> 值类型为dict，
> 存储用户信息：'id','authentication','birthday','brief_introduction','city','fans_num',
>             'follows_num','gender','labels','province','sentiment','sex_orientation',
>             'tweets_num','vip_level'，
> 内容参考来源:CommentUsers2020.csv
> 示例：{"7007025883":{
>                     'id': '7007025883',
>                     ’nick_name‘: ,
>                     'authentication': nan,
>                     'birthday': nan,
>                     'brief_introduction': nan,
>                     'city': nan,
>                     'fans_num': 94.0,
>                     'follows_num': 203.0,
>                     'gender': '男',
>                     'labels': nan,
>                     'province': '其他',
>                     'tweets_num': 33346.0,
>                     'vip_level': '未开通'
>                     }
> ```

##### self.fc2020: list

> ```
> 每个元素也为一个list（长度为7， 类型均为str），
> 存储：微博内容id，用户id和内容，发布时间，点赞数，转发或评论类型，内容唯一id,
> 内容来源参考：Comments2020.csv
> 示例：
> [
>     ['JzvPXy4VI',
>      '5044677789',
>      '正是、正是！生命除了自渡自救、上帝我佛好像也是爱莫能助；人生早已为我们设伏了一场场考验拷问、颠覆与救赎乃为生命注定的一段段阳光下的冷战！无处不在的对峙战场、让我们活像一只只在燃烧地板上热舞的蚁、别有一番滋味心头！我说与其在沉沦中失意自戕、不如上演一场慷慨的悲情仪式。',
>      '2020-12-22 00:23:41',
>      '1',
>      'C',
>      'C_4584728101913123']
>     ...
> ]
> ```

##### self.fcemotion: dict

> ```
> 键值为内容唯一id,
> 内容为情感标签，
> 内容来源参考：fc_emotion.csv,
> 示例：{"C_4584728101913123": 2, ...}
> ```

## FILE: dataprocess.py

### class: CommunicationMap

This class is used to generate propagation graph data

#### Incoming parameters

- ori_data: list
- user_info: dict
- forward_info: dict
- forward_users_info: dict
- emotion: dict

#### Introduction to return parameters

##### self.info: dict

> ```
> 键值为微博内容id，
> 值为dict，存储传播链上各种信息
> 具体见下传播图数据结构
> 
>  """
>  传播图数据结构
>     - 原微博(`info["content"], info["data"]["name"]`)
>     - 传播层级(`info["rank_num"]`)
>     - 每一级的数量(`info["ranki_num"]`)
>     - 每一层内容，父亲是谁(`info["data"]`)
>     - user_id,信息(`info["user"], info["data"]["children"][i]["name"], info["data"]["children"][i]["user"]`)
>     info = {"content_id":{
>                             "content":xxx, 
>                             "content_id":xxx, 
>                             "user":{
>                                 "id":xxx,
>                                 ...,
>                             }, 
>                             "emotion":{
>                                 "value":xxx,
>                                 ...
>                             },
>                             "forward_num":xxx,
>                             "rank_num": xxx, 
>                             "rank1_num":xxx,
>                             ..., 
>                             "rankn_num":xxx,
>                             "influence":xxx
>                             "data" = {
>                                 "name":xxx,
>                                 "children":[
>                                 {"name":xxx,"user":{...}, "value":xxx, "key_words"=[...], "children":[...]},
>                                 ...,
>                                 {"name":xxx,"user":{...}, "value":xxx, "key_words"=[...], "children":[...]}
>                                 ],
>                             }
>                         }
>                 ...
>                 }
>     """
> ```

### class: Overview

This class is used to generate overview data

#### Incoming parameters

- ori_data: list
- users_info: dict
- time: dict
- topic: dict

#### Introduction to return parameters

##### self.map2time: dict

> ```
> 键值为地点（用户信息中的provence），
> 值类型list，
> 存储微博发布时间，微博内容id
> 示例：{"北京":[['2020-01-02', 'InzJsiQ1k'],
>              ['2020-01-06', 'IocdREafF'],
>              ['2020-01-05', 'Io7AU2ycs'],
>              ['2020-01-06', 'IofEGwaKE'],
>              ['2020-01-06', 'IofwIrUtu'],
>              ['2020-01-07', 'IopyFzr9w'],
>              ['2020-01-12', 'Ip8XldyDf'],
>              ['2020-01-16', 'IpMREzpOH'],
>              ['2020-01-24', 'IqV15ahlk'],
>              ['2020-01-25', 'Ir6u5gIxd'],
>              ['2020-01-25', 'Ir778sKuy'],
>              ['2020-01-23', 'IqM32E8p5'],
>              ['2020-01-30', 'IrMIRznEW'],
>              ['2020-01-29', 'IrMqcEx6H'],
>              ['2020-01-30', 'IrSHmwvB6'],
>              ['2020-01-30', 'IrQi3DiOs'],
>              ['2020-04-07', 'ICdWpg0IX'],
>              ['2020-02-04', 'IsB3JDMV2'],
>              ['2020-02-03', 'IsvRpxVil'],
>              ['2020-02-04', 'IsDS2Eef9'],
>              ['2020-02-04', 'IsFIj88qO'],
>              ['2020-02-05', 'IsHpmkE51'],
>              ['2020-02-05', 'IsPsJoISU'],
>              ['2020-02-05', 'IsMlnB2RX'],
>              ['2020-02-05', 'IsN1B4FUy'],
>              ['2020-02-06', 'IsXvm61SV'],
>              ['2020-02-08', 'ItfahfwiH'],
>              ['2020-02-04', 'IsFyVg476'],
>              ['2020-02-05', 'IsIHQ40OZ'],
>              ['2020-02-06', 'IsXtL5RkV'],
>              ['2020-02-10', 'ItzIArnqd'],
>              ['2020-02-12', 'ItSii4Hrr'],
>              ['2020-02-16', 'Iuw7fA7E4'],
>              ['2020-02-20', 'Iv2FZ9vJP'],
>              ['2020-02-20', 'IuZ0rtfQ1'],
>              ['2020-02-24', 'IvIluwxDH'],
>              ['2020-02-25', 'IvOA9dNTp'],
>              ['2020-02-25', 'IvMM8zuPA'],
>              ['2020-02-24', 'IvHq82cRT'],
>              ['2020-02-29', 'IwqT2lIyz'],
>              ['2020-02-26', 'Iw1BhEBNC'],
>              ['2020-02-26', 'Iw1Ra1oFX'],
>              ['2020-02-23', 'Ivw9zqfkm'],
>              ['2020-03-02', 'IwF8Llkmx'],
>              ['2020-03-09', 'IxPl2a2eG'],
>              ['2020-03-09', 'IxQpX9dIb'],
>              ['2020-03-09', 'IxQw8FtbG'],
>              ['2020-03-09', 'IxP6keKj1'],
>              ['2020-03-09', 'IxQ5G8ird'],
>              ['2020-03-09', 'IxReD7IVL'],
>              ['2020-03-12', 'IygTXyus4'],
>              ['2020-03-12', 'IyidsaZ3T'],
>              ['2020-03-12', 'Iyh2SrmDY'],
>              ['2020-03-14', 'IytQFcFmm'],
>              ['2020-03-15', 'IyJt1AelP'],
>              ['2020-03-16', 'IyPIP94ky'],
>              ['2020-03-16', 'IySaAwmqa'],
>              ['2020-03-16', 'IyRLwd5jh'],
>              ['2020-03-17', 'Iz02W5Tpd'],
>              ['2020-03-20', 'IzuCjubDz'],
>              ['2020-03-20', 'IzuoblfF4'],
>              ['2020-03-20', 'IzvkH56Xi'],
>              ['2020-03-20', 'IzwAdzwZV'],
>              ['2020-03-20', 'IztH91Qbj'],
>              ['2020-03-20', 'IzwVWo1Ya'],
>              ['2020-03-21', 'IzAj4iREj'],
>              ['2020-03-21', 'IzB3Bv6Jt'],
>              ['2020-03-21', 'IzCfY2fXp'],
>              ['2020-03-22', 'IzLr8BOAl'],
>              ['2020-03-21', 'IzDheq4Cc'],
>              ['2020-03-22', 'IzPMyugqb'],
>              ['2020-03-22', 'IzK7fq2Z6'],
>              ['2020-03-22', 'IzPGw5rId'],
>              ['2020-03-22', 'IzP72bx5M'],
>              ['2020-03-22', 'IzQ0krsjZ'],
>              ['2020-03-22', 'IzPd6kgEn'],
>              ['2020-03-22', 'IzOYW8JeB'],
>              ['2020-03-22', 'IzP66xfdE'],
>              ['2020-03-21', 'IzDH0p22z'],
>              ['2020-03-21', 'IzGaIl6Nt'],
>              ['2020-03-22', 'IzONJnU5S'],
>              ['2020-03-28', 'IAJfLFv4k'],
>              ['2020-04-01', 'IBk3XqZaH'],
>              ['2020-03-28', 'IAHFQw1e6'],
>              ['2020-03-31', 'IBcnwyKzY'],
>              ['2020-04-06', 'IC6daFpNE'],
>              ['2020-04-05', 'IBTM0AduR'],
>              ['2020-04-06', 'IC2MZCZpw'],
>              ['2020-04-06', 'IC7EV6zN2'],
>              ['2020-04-06', 'IC7gYveY1'],
>              ['2020-04-10', 'ICDmDgy92'],
>              ['2020-04-11', 'ICNET0BKt'],
>              ['2020-04-11', 'ICNtMbOPk'],
>              ['2020-04-06', 'IC6NzBmW0'],
>              ['2020-04-10', 'ICHFWwp9f'],
>              ['2020-04-11', 'ICQnvfwBv'],
>              ['2020-04-09', 'ICyZh9nMn'],
>              ['2020-04-12', 'ID1W814I4'],
>              ['2020-04-22', 'IEtkApmJf'],
>              ['2020-04-10', 'ICD11yPYB'],
>              ['2020-04-23', 'IEEiACA2z'],
>              ['2020-05-02', 'J02kr40LW'],
>              ['2020-05-01', 'IFSz1Cxkz'],
>              ['2020-05-11', 'J1oL7dFLn'],
>              ['2020-05-11', 'J1opr2Aw4'],
>              ['2020-05-11', 'J1o6XCyta'],
>              ['2020-05-11', 'J1oqjmhZ1'],
>              ['2020-05-11', 'J1ocjbNUW'],
>              ['2020-05-12', 'J1ApkA6zp'],
>              ['2020-05-12', 'J1zIvzaiw'],
>              ['2020-05-16', 'J29tXmNyL'],
>              ['2020-05-19', 'J2Bit2nkE'],
>              ['2020-05-26', 'J3CFUhxbZ'],
>              ['2020-05-28', 'J3VbhEvWq'],
>              ['2020-05-13', 'J1JwZ3Cci'],
>              ['2020-06-03', 'J4SPy0xUQ'],
>              ['2020-06-04', 'J58mUDD9h'],
>              ['2020-06-04', 'J57H57Zo8'],
>              ['2020-06-04', 'J57sC2VCs'],
>              ['2020-06-05', 'J5bL1rFFv'],
>              ['2020-06-04', 'J57pYngJa'],
>              ['2020-06-05', 'J5ckfaYmk'],
>              ['2020-06-05', 'J5dVVpeUz'],
>              ['2020-06-06', 'J5qk8wG6J'],
>              ['2020-06-09', 'J5NArdbo4'],
>              ['2020-06-09', 'J5LKicrNq'],
>              ['2020-06-11', 'J67Q22COi'],
>              ['2020-06-13', 'J6qUk8edj'],
>              ['2020-06-13', 'J6qgJrUZh'],
>              ['2020-06-14', 'J6zLqEkjE'],
>              ['2020-06-15', 'J6I36dAzy'],
>              ['2020-06-15', 'J6J7NzHzD'],
>              ['2020-06-17', 'J6ZmRrBuj'],
>              ['2020-06-17', 'J74SJDkr8'],
>              ['2020-06-15', 'J6MCA7Aft'],
>              ['2020-06-18', 'J7bdllqjg'],
>              ['2020-06-12', 'J6jVrvZ3g'],
>              ['2020-06-17', 'J75EM9KG6'],
>              ['2020-06-18', 'J7as0h1Xa'],
>              ['2020-06-18', 'J7cyq8hfk'],
>              ['2020-06-19', 'J7kRnrsRY'],
>              ['2020-06-19', 'J7p1WbOCg'],
>              ['2020-06-23', 'J7WXO8iso'],
>              ['2020-06-26', 'J8pIKeBPn'],
>              ['2020-01-21', 'IqwTOEpoi'],
>              ['2020-06-30', 'J91xcl7yL'],
>              ['2020-04-30', 'IFKI69e5Q'],
>              ['2020-06-30', 'J93gzpG01'],
>              ['2020-07-03', 'J9swl7cZz'],
>              ['2020-07-03', 'J9sAoCLrR'],
>              ['2020-07-03', 'J9sD4DfKY'],
>              ['2020-07-03', 'J9sLN97dr'],
>              ['2020-07-03', 'J9t7ODSGW'],
>              ['2020-07-03', 'J9ryVguEX'],
>              ['2020-07-02', 'J9m5toaXL'],
>              ['2020-07-06', 'J9VUZfLe7'],
>              ['2020-07-07', 'Ja4sHbtT2'],
>              ['2020-07-08', 'Jagelfi7p'],
>              ['2020-07-15', 'JbefauR1p'],
>              ['2020-07-18', 'JbMVXvAa0'],
>              ['2020-07-24', 'JcIyT4rwm'],
>              ['2020-07-24', 'JcJpkk42z'],
>              ['2020-07-24', 'JcH92xF0i'],
>              ['2020-07-25', 'JcQwHwgrK'],
>              ['2020-07-27', 'Jd6L4vQzd'],
>              ['2020-08-07', 'JeMZD7OE5'],
>              ['2020-08-07', 'JeO8UxH5e'],
>              ['2020-07-01', 'J98gAzg9A'],
>              ['2020-08-09', 'Jf6We7zOq'],
>              ['2020-08-15', 'Jg0zLjsrG'],
>              ['2020-08-16', 'Jg7RR6Cy7'],
>              ['2020-08-16', 'JgbebFuvp'],
>              ['2020-08-18', 'Jgon388zL'],
>              ['2020-08-19', 'JgCAns36c'],
>              ['2020-08-19', 'JgDLdbRYk'],
>              ['2020-08-22', 'Jh4oMEVzk'],
>              ['2020-08-28', 'Ji17a26JI'],
>              ['2020-09-18', 'JlaFcEJaE'],
>              ['2020-09-18', 'JlauTefHK'],
>              ['2020-09-18', 'JlbnxlYRe'],
>              ['2020-09-23', 'JlXMCk3LG'],
>              ['2020-10-07', 'Jo8Ap4Yqo'],
>              ['2020-10-08', 'Johpe9xLb'],
>              ['2020-10-08', 'Johtxwo9g'],
>              ['2020-10-09', 'JolEA5pUd'],
>              ['2020-10-10', 'JowPJisZf'],
>              ['2020-10-08', 'Joi1Khh5g'],
>              ['2020-09-23', 'JlYCh8eLf'],
>              ['2020-10-12', 'JoOeS3B0R'],
>              ['2020-10-13', 'JoWtiDMe8'],
>              ['2020-10-18', 'JpJGRu6Fs'],
>              ['2020-10-19', 'JpRCR6JRS'],
>              ['2020-10-18', 'JpMUgfOTx'],
>              ['2020-10-18', 'JpOiq7Yaq'],
>              ['2020-10-16', 'JpoP5sclS'],
>              ['2020-10-27', 'Jr9IUsAad'],
>              ['2020-10-25', 'JqQaIp8cD'],
>              ['2020-10-25', 'JqRs4B9rp'],
>              ['2020-10-24', 'JqIZRufQp'],
>              ['2020-10-28', 'JrbKe8OAG'],
>              ['2020-11-07', 'JsQ6IjH3p'],
>              ['2020-11-10', 'JtdsnbpCF'],
>              ['2020-11-13', 'JtGDgfGoL'],
>              ['2020-11-14', 'JtRm3bw8d'],
>              ['2020-11-16', 'Ju8fM4ILB'],
>              ['2020-02-06', 'IsY04fR3M'],
>              ['2020-12-08', 'JxuqljyzN'],
>              ['2020-12-08', 'JxwG1o8bA'],
>              ['2020-12-08', 'Jxw8e0VIx'],
>              ['2020-12-12', 'Jy6mxDpNh'],
>              ['2020-12-12', 'Jyan9nyyx']]
>     ...
>     }
> ```

##### self.time2topic: dict

> ```
> 键值为时间，
> 值类型dict，
> 存储每个主题下微博数量和对应id
> 示例：{"2020-02-06":{"date":"2020-02-06",
>                     "topic":[{
>                             'name': '社会时事':
>                             'num': 7,
>                             'id': ['IsRuG67sY',
>                             'IsUXlDx2E',
>                             'IsWGuh4Fv',
>                             'IsXvm61SV',
>                             'IsZPNhHLP',
>                             'IsXtL5RkV',
>                             'IsXYBvMDu'],
>                              }
>                             ...
>                             ]
>                     }
>     ...
>     }
> ```

### class: Middlelevel

This class is used to generate middlelevel data

#### Incoming parameters

- ori_data: list
- time: dict
- topic: dict
- emotion: dict
- influence: dict

#### Introduction to return parameters

##### self.circle: dict

> ```
> 键值为微博内容id，
> 值为dict，
> 存储发布时间，情感，主题，长度，影响力信息，
> 示例：{"InzJsiQ1k"：{'time': '2020-01-02',
>                      'topic': '社会时事',
>                      'emotion': {'value': '-1',
>                       'positive_prob': 0.000159879,
>                       'negative_prob': 0.99984},
>                      'length': 181,
>                      'influence': 30.0
>                     }
>     ...
>     }
> ```

### class: NewCommunicationMap

#### Introduction to return parameters

##### self.info: dict

> ```
> 键值为微博内容id,
> 内容为id，内容，发表时间，用户信息，情感信息，评论信息
> 示例：{'InzJsiQ1k': {'content_id': 'InzJsiQ1k',
>          'content': '#毽客视线#一位河南省政府官员，在高速公路付费通道时拿错了银行卡，刷卡后当即被爆露卡上的巨大余额，一个星期后就被双规！😂 这时你就该知道官员财产申报和公示为什么提出来这么多年却迟迟没有下文 ，因为不但干净的人太少了，而且一个赛一个能贪，真要通过了那不是革自己的命吗？按说抓了那么多老虎，应该收敛一点才是，怎么还是层出不穷[抓狂]为什么…… 毽客逆风飞扬的微博视频',
>          'created_at': '2020-01-02 07:35:18    ',
>          'user_info': {'id': '1202586970',
>           'authentication': None,
>           'birthday': '2013-10-12',
>           'brief_introduction': '一个还赖在尘世中的修行者，只因还有一份责任和使命感。',
>           'city': None,
>           'fans_num': 222153,
>           'follows_num': 19,
>           'gender': '男',
>           'labels': '自由,情感,个性',
>           'province': '北京',
>           'sentiment': None,
>           'sex_orientation': None,
>           'tweets_num': 4840,
>           'vip_level': '：6级'},
>          'emotion': {'value': '-1',
>           'positive_prob': 0.000159879,
>           'negative_prob': 0.99984},
>          'data': [{'fc_user': {'id': '7007025883',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': None,
>             'fans_num': 94,
>             'follows_num': 203,
>             'gender': '男',
>             'labels': None,
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': 33346,
>             'vip_level': '：未开通'},
>            'content': '大雄42193://@美丽的和谐家园8868://@用户蓝天彩虹6389479884:转发微博',
>            'created_at': '2020-01-04 13:13:25',
>            'like_num': '1',
>            'C_F': 'F',
>            'emotion': '1'},
>           {'fc_user': {'id': '6187132230',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': '不入群！天下为公！传播正能量！信仰毛泽东！让世界充满爱！！！',
>             'city': None,
>             'fans_num': 8726,
>             'follows_num': 4989,
>             'gender': '男',
>             'labels': None,
>             'province': '河北',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': 83672,
>             'vip_level': '：1级'},
>            'content': '美丽的和谐家园8868://@用户蓝天彩虹6389479884:转发微博',
>            'created_at': '2020-01-04 12:53:44',
>            'like_num': '6',
>            'C_F': 'F',
>            'emotion': '1'},
>           {'fc_user': {'id': '6389479884',
>             'authentication': None,
>             'birthday': '1979-02-16',
>             'brief_introduction': '其他',
>             'city': None,
>             'fans_num': '730',
>             'follows_num': '858',
>             'gender': '男',
>             'labels': None,
>             'province': '广东',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '2392',
>             'vip_level': '：未开通'},
>            'content': '用户蓝天彩虹6389479884:转发微博',
>            'created_at': '2020-01-02 21:20:23',
>            'like_num': '28',
>            'C_F': 'F',
>            'emotion': '1'},
>           {'fc_user': {'id': '6006625578',
>             'authentication': None,
>             'birthday': '1985-02-20',
>             'brief_introduction': '只关注喜欢的人',
>             'city': '东城区',
>             'fans_num': '38',
>             'follows_num': '28',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '3505',
>             'vip_level': '：未开通'},
>            'content': '靠谱的钟爱一生585:[赞啊][求关注][好喜欢]',
>            'created_at': '2020-01-02 09:49:02',
>            'like_num': '0',
>            'C_F': 'F',
>            'emotion': '2'},
>           {'fc_user': {'id': '5869967115',
>             'authentication': None,
>             'birthday': '1979-07-21',
>             'brief_introduction': '做最好的你，云淡风轻。',
>             'city': None,
>             'fans_num': '70',
>             'follows_num': '30',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '7848',
>             'vip_level': '：未开通'},
>            'content': '一江春水落花流:它們可以如此的囂張， 全歸功於人們的縱容。',
>            'created_at': '2020-01-02 09:32:58',
>            'like_num': '0',
>            'C_F': 'F',
>            'emotion': '2'},
>           {'fc_user': {'id': '1548434974',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': None,
>             'fans_num': 19,
>             'follows_num': 20,
>             'gender': '男',
>             'labels': '哲学,北京',
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': 3216,
>             'vip_level': '：未开通'},
>            'content': '手机用户4349749793_681:[偷笑]',
>            'created_at': '2020-01-02 09:29:37',
>            'like_num': '0',
>            'C_F': 'F',
>            'emotion': '2'},
>           {'fc_user': {'id': '7161003036',
>             'authentication': None,
>             'birthday': '1998-02-23',
>             'brief_introduction': None,
>             'city': None,
>             'fans_num': '17',
>             'follows_num': '10',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1458',
>             'vip_level': '：未开通'},
>            'content': '小蜜蜂哇哇叫:[哆啦A梦微笑][哆啦A梦吃惊]',
>            'created_at': '2020-01-02 08:45:05',
>            'like_num': '0',
>            'C_F': 'F',
>            'emotion': '2'},
>           {'fc_user': {'id': '1109305345',
>             'authentication': None,
>             'birthday': '天蝎座',
>             'brief_introduction': '唯美食不可拒绝',
>             'city': '东城区',
>             'fans_num': '785',
>             'follows_num': '1893',
>             'gender': '男',
>             'labels': '重庆生活,好书,军事天地',
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '8320',
>             'vip_level': '：未开通'},
>            'content': '迷迷糊糊地转:这事是真的呀？',
>            'created_at': '2020-01-02 08:38:09',
>            'like_num': '1',
>            'C_F': 'F',
>            'emotion': '0'},
>           {'fc_user': {'id': '5165089330',
>             'authentication': None,
>             'birthday': '1970-01-01',
>             'brief_introduction': None,
>             'city': '东城区',
>             'fans_num': '447',
>             'follows_num': '181',
>             'gender': '女',
>             'labels': '北京生活,幽默,文学',
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '8984',
>             'vip_level': '：未开通'},
>            'content': '樱淼的微博:应该把权力扼杀在摇篮！',
>            'created_at': '2020-01-02 07:51:40',
>            'like_num': '1',
>            'C_F': 'F',
>            'emotion': '0'},
>           {'fc_user': {'id': '5450035157',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '开封',
>             'fans_num': 12,
>             'follows_num': 488,
>             'gender': '女',
>             'labels': None,
>             'province': '河南',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': 55,
>             'vip_level': '：未开通'},
>            'content': '天蝎座的夏美:转发微博',
>            'created_at': '2020-01-02 07:45:08',
>            'like_num': '1',
>            'C_F': 'F',
>            'emotion': '1'},
>           {'fc_user': {'id': '1409455782',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '成都',
>             'fans_num': '116',
>             'follows_num': '546',
>             'gender': '男',
>             'labels': '美食,微博奇葩,新闻趣事',
>             'province': '四川',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '334',
>             'vip_level': '：未开通'},
>            'content': '槐花几时开666:德国人创立/的学说没有在德国发展起来，却在亚洲大放异彩，几十年来培养了无数的捞钱人才。',
>            'created_at': '2020-01-02 07:42:12',
>            'like_num': '1',
>            'C_F': 'F',
>            'emotion': '2'},
>           {'fc_user': {'id': '3031121830',
>             'authentication': None,
>             'birthday': '1900-12-31',
>             'brief_introduction': '世界是复杂的，你看到的很可能只是一面，甚至只是一角。',
>             'city': None,
>             'fans_num': '130',
>             'follows_num': '118',
>             'gender': '女',
>             'labels': '教育就业,健康,新闻资讯',
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1153',
>             'vip_level': '：4级'},
>            'content': '拿着这么多钱寝食难安啊，就像是一个不知啥时会爆炸的炸弹💣，有得必有失[允悲]',
>            'created_at': '2020-01-02 18:44:11',
>            'like_num': '1',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5359652717',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': None,
>             'fans_num': '1',
>             'follows_num': '53',
>             'gender': '男',
>             'labels': '名人明星',
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '7',
>             'vip_level': '：未开通'},
>            'content': '真是什么人都有，刷银行卡余额会显示在屏幕上？',
>            'created_at': '2020-01-04 23:06:40',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '6389479884',
>             'authentication': None,
>             'birthday': '1979-02-16',
>             'brief_introduction': '其他',
>             'city': None,
>             'fans_num': '730',
>             'follows_num': '858',
>             'gender': '男',
>             'labels': None,
>             'province': '广东',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '2392',
>             'vip_level': '：未开通'},
>            'content': '新年好[作揖][作揖]腊八节快乐[鲜花]',
>            'created_at': '2020-01-02 21:23:16',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '3031121830',
>             'authentication': None,
>             'birthday': '1900-12-31',
>             'brief_introduction': '世界是复杂的，你看到的很可能只是一面，甚至只是一角。',
>             'city': None,
>             'fans_num': '130',
>             'follows_num': '118',
>             'gender': '女',
>             'labels': '教育就业,健康,新闻资讯',
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1153',
>             'vip_level': '：4级'},
>            'content': '回复@毽客逆风飞扬:所以还是胆子小的好，晚上睡觉安心[允悲]',
>            'created_at': '2020-01-02 18:54:28',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '3031121830',
>             'authentication': None,
>             'birthday': '1900-12-31',
>             'brief_introduction': '世界是复杂的，你看到的很可能只是一面，甚至只是一角。',
>             'city': None,
>             'fans_num': '130',
>             'follows_num': '118',
>             'gender': '女',
>             'labels': '教育就业,健康,新闻资讯',
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1153',
>             'vip_level': '：4级'},
>            'content': '回复@毽客逆风飞扬:这样的例子太多了',
>            'created_at': '2020-01-02 18:45:39',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5303576627',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '苏州',
>             'fans_num': '599',
>             'follows_num': '91',
>             'gender': '女',
>             'labels': '其他生活',
>             'province': '江苏',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '739',
>             'vip_level': '：未开通'},
>            'content': '回复@毽客逆风飞扬:不止的，算不过来[允悲][允悲]',
>            'created_at': '2020-01-02 18:39:06',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5303576627',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '苏州',
>             'fans_num': '599',
>             'follows_num': '91',
>             'gender': '女',
>             'labels': '其他生活',
>             'province': '江苏',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '739',
>             'vip_level': '：未开通'},
>            'content': '回复@毽客逆风飞扬:我在算着，能买多少猫粮[偷笑][嘻嘻][嘻嘻]',
>            'created_at': '2020-01-02 18:32:26',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '5303576627',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '苏州',
>             'fans_num': '599',
>             'follows_num': '91',
>             'gender': '女',
>             'labels': '其他生活',
>             'province': '江苏',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '739',
>             'vip_level': '：未开通'},
>            'content': '回复@毽客逆风飞扬:这卡太重了[哈哈][哈哈]',
>            'created_at': '2020-01-02 18:29:43',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '5303576627',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '苏州',
>             'fans_num': '599',
>             'follows_num': '91',
>             'gender': '女',
>             'labels': '其他生活',
>             'province': '江苏',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '739',
>             'vip_level': '：未开通'},
>            'content': '这是多少钱啊？看了几遍!这贪的不是一般的多[笑cry][笑cry]',
>            'created_at': '2020-01-02 17:58:58',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5536252113',
>             'authentication': None,
>             'birthday': '天蝎座',
>             'brief_introduction': '善待生命，不负年华',
>             'city': '沈阳',
>             'fans_num': '3891',
>             'follows_num': '356',
>             'gender': '女',
>             'labels': None,
>             'province': '辽宁',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1145',
>             'vip_level': '：未开通'},
>            'content': '贪官，一不小心就露馅了！',
>            'created_at': '2020-01-02 11:40:23',
>            'like_num': '1',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5274877051',
>             'authentication': None,
>             'birthday': '处女座',
>             'brief_introduction': '努力学习，提高自身价值。好心态，让生活充满阳光。',
>             'city': '美国',
>             'fans_num': '3488',
>             'follows_num': '2000',
>             'gender': '女',
>             'labels': '幽默,开朗,热爱生活',
>             'province': '海外',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '440',
>             'vip_level': '：未开通'},
>            'content': '飞扬哥腊八节快乐[礼物][音乐][鲜花]',
>            'created_at': '2020-01-02 11:19:23',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '6006625578',
>             'authentication': None,
>             'birthday': '1985-02-20',
>             'brief_introduction': '只关注喜欢的人',
>             'city': '东城区',
>             'fans_num': '38',
>             'follows_num': '28',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '3505',
>             'vip_level': '：未开通'},
>            'content': '[赞啊][求关注][好喜欢]',
>            'created_at': '2020-01-02 09:49:02',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '5869967115',
>             'authentication': None,
>             'birthday': '1979-07-21',
>             'brief_introduction': '做最好的你，云淡风轻。',
>             'city': None,
>             'fans_num': '70',
>             'follows_num': '30',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '7848',
>             'vip_level': '：未开通'},
>            'content': '它們可以如此的囂張， 全歸功於人們的縱容。',
>            'created_at': '2020-01-02 09:32:58',
>            'like_num': '1',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '5501639437',
>             'authentication': None,
>             'birthday': '2015-01-02',
>             'brief_introduction': '过平淡生活',
>             'city': '成都',
>             'fans_num': '481',
>             'follows_num': '58',
>             'gender': '女',
>             'labels': '旅游',
>             'province': '四川',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1843',
>             'vip_level': '：5级'},
>            'content': '飞扬哥蜡儿快乐！',
>            'created_at': '2020-01-02 09:31:47',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '5710975136',
>             'authentication': None,
>             'birthday': '2018-07-30',
>             'brief_introduction': '日出  ོ 踏浪   ོ 海鲜   ོ 啤酒 •͈ᴗ•͈◞︎♡ 🦀🐚👦🌟🌈🏄💨海风咸咸的，吹散你我身旁的烦恼！🙏',
>             'city': None,
>             'fans_num': '11102',
>             'follows_num': '2785',
>             'gender': '女',
>             'labels': None,
>             'province': '其他',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '385',
>             'vip_level': '：6级'},
>            'content': '新年阳光明媚，新岁已登场。过了腊八就是年啦，祝福腊八节快乐，今天喝粥呦~老师早上好[太阳][鲜花][鲜花][鲜花]',
>            'created_at': '2020-01-02 08:54:59',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '7161003036',
>             'authentication': None,
>             'birthday': '1998-02-23',
>             'brief_introduction': None,
>             'city': None,
>             'fans_num': '17',
>             'follows_num': '10',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '1458',
>             'vip_level': '：未开通'},
>            'content': '[哆啦A梦微笑][哆啦A梦吃惊]',
>            'created_at': '2020-01-02 08:45:05',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '1109305345',
>             'authentication': None,
>             'birthday': '天蝎座',
>             'brief_introduction': '唯美食不可拒绝',
>             'city': '东城区',
>             'fans_num': '785',
>             'follows_num': '1893',
>             'gender': '男',
>             'labels': '重庆生活,好书,军事天地',
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '8320',
>             'vip_level': '：未开通'},
>            'content': '这事是真的呀？',
>            'created_at': '2020-01-02 08:38:09',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '5165089330',
>             'authentication': None,
>             'birthday': '1970-01-01',
>             'brief_introduction': None,
>             'city': '东城区',
>             'fans_num': '447',
>             'follows_num': '181',
>             'gender': '女',
>             'labels': '北京生活,幽默,文学',
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '8984',
>             'vip_level': '：未开通'},
>            'content': '应该把权力扼杀在摇篮！',
>            'created_at': '2020-01-02 07:51:40',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'},
>           {'fc_user': {'id': '1409455782',
>             'authentication': None,
>             'birthday': None,
>             'brief_introduction': None,
>             'city': '成都',
>             'fans_num': '116',
>             'follows_num': '546',
>             'gender': '男',
>             'labels': '美食,微博奇葩,新闻趣事',
>             'province': '四川',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '334',
>             'vip_level': '：未开通'},
>            'content': '回复@毽客逆风飞扬:这就是培养出来的好干部。',
>            'created_at': '2020-01-02 07:43:16',
>            'like_num': '1',
>            'C_F': 'C',
>            'emotion': '2'},
>           {'fc_user': {'id': '6429659229',
>             'authentication': None,
>             'birthday': '2017-12-10',
>             'brief_introduction': '不服来战',
>             'city': None,
>             'fans_num': '39',
>             'follows_num': '19',
>             'gender': '女',
>             'labels': None,
>             'province': '北京',
>             'sentiment': None,
>             'sex_orientation': None,
>             'tweets_num': '2573',
>             'vip_level': '：未开通'},
>            'content': '[困][哈欠]',
>            'created_at': '2020-01-02 07:36:31',
>            'like_num': '0',
>            'C_F': 'C',
>            'emotion': '0'}]}
> ...
> }
> ```