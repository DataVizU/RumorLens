import numpy as np
from sklearn import manifold
import math
import copy
import hashlib
from data_process.tf_idf import tfidf, participle


def flow_kew_words(ids, ori_data, topic):
    months_topic_keywords = {}
    months_texts_topic = {}
    for id in ids:
        for i in ori_data:
            if id == i[0]:
                created_time = int(copy.deepcopy(i[7]).split("-")[1])
                if created_time not in months_texts_topic.keys():
                    months_texts_topic[created_time] = {}
                if topic[id]['topic'] not in months_texts_topic[created_time].keys():
                    months_texts_topic[created_time][topic[id]['topic']] = []
                months_texts_topic[created_time][topic[id]['topic']].append(copy.deepcopy(i[2]))
                break
    for mo in months_texts_topic:
        months_topic_keywords[mo] = {}
        for to in months_texts_topic[mo]:
            sentences = participle(copy.deepcopy(months_texts_topic[mo][to]))
            if len(sentences) > 1:
                months_topic_keywords[mo][to] = tfidf(sentences)
    return months_topic_keywords


class CommunicationMap(object):
    """
    用于生成传播图数据

    传入参数类简介：
    ori_data:list

    user_info:dict,

    forward_info:dict，

    forward_users_info:dict,

    emotion:dict,

    返回参数简介：
    self.info:dict
            键值为微博内容id，
            值为dict，存储传播链上各种信息

    """

    def __init__(self):
        self.info = {}

    def creat(self, ori_data: list, user_info: dict, forward_info: dict, forward_user_info: dict, emotion: dict,
              time: dict, fc2020: list, commentusers: dict, fcemotion: dict, topic: dict):

        global name

        def add_influence():
            alpha = [30.0, 7.0, 11.0, 11.0, 11.0, 10.0, 20.0]
            # 类别， 浏览数， 点赞数， 评论局部， 评论数， 转发局部， 转发
            alpha_province = {"安徽": 0.017,
                              "澳门": 0.023,
                              "北京": 0.26,
                              "福建": 0.020,
                              "甘肃": 0.005,
                              "广东": 0.095,
                              "广西": 0.014,
                              "贵州": 0.004,
                              "海南": 0.005,
                              "河北": 0.029,
                              "河南": 0.026,
                              "黑龙江": 0.012,
                              "湖北": 0.024,
                              "湖南": 0.024,
                              "吉林": 0.012,
                              "江苏": 0.048,
                              "江西": 0.017,
                              "辽宁": 0.033,
                              "内蒙古": 0.008,
                              "宁夏": 0.003,
                              "青海": 0.002,
                              "山东": 0.049,
                              "山西": 0.013,
                              "陕西": 0.016,
                              "上海": 0.045,
                              "四川": 0.028,
                              "台湾": 0.023,
                              "天津": 0.011,
                              "西藏": 0.001,
                              "香港": 0.023,
                              "新疆": 0.006,
                              "云南": 0.010,
                              "浙江": 0.065,
                              "重庆": 0.017,
                              "海外": 0.002,
                              "其他": 0.010,
                              }
            new_communication_map_data = \
                NewCommunicationMap().creat(ori_data, time, user_info, emotion, fc2020, commentusers, forward_user_info,
                                            fcemotion)

            all_view = []
            all_comment = []
            all_forward = []
            all_like = []

            for i in range(len(ori_data)):
                # 评论计数
                comments = []
                see_comments_num = 0
                for fc in new_communication_map_data[ori_data[i][0]]['data']:
                    if fc['C_F'] == 'C':
                        comments.append(fc)
                        see_comments_num += 1

                # 转发计数
                see_forwards_num = 0
                if "rank1_num" in self.info[ori_data[i][0]].keys():
                    forward = [self.info[ori_data[i][0]]["data"]["children"][j] for j in
                               range(self.info[ori_data[i][0]]["rank1_num"])]
                    for k in forward:
                        if k["children"] != []:
                            for l in k["children"]:
                                if l not in forward:
                                    forward.append(l)
                    see_forwards_num = len(forward)

                all_comment.append(see_comments_num)
                all_forward.append(see_forwards_num)
                all_like.append(int(ori_data[i][4]))
                all_view.append(math.sqrt(all_comment[-1] + all_forward[-1] + all_like[-1]))

            view_max = np.array(all_view).max()
            comment_max = np.array(all_comment).max()
            forward_max = np.array(all_forward).max()
            like_max = np.array(all_like).max()

            for i in range(len(ori_data)):
                #     print(ori_data[i][0])
                #     print(all_comment[i], all_forward[i], all_like[i])

                influence = 0.0
                # 类别得分
                if topic[ori_data[i][0]]["topic"] in ['社会时事', '国际', '军事']:
                    influence += alpha[0] * 1.0
                elif topic[ori_data[i][0]]["topic"] in ['娱乐', '科技', '常识', '教育']:
                    influence += alpha[0] * 0.8
                else:
                    influence += alpha[0] * 0.7
                # 浏览数得分
                influence += alpha[1] * min(1, all_view[i] / view_max)
                #     print(influence)

                # 评论全局得分
                influence += alpha[4] * min(1, all_comment[i] / comment_max)
                #     print(influence)

                # 转发全局得分
                influence += alpha[6] * min(1, all_forward[i] / forward_max)
                #     print(influence)

                # 点赞得分
                influence += alpha[2] * min(1, all_like[i] / 10000)

                #     print(influence)

                # 评论局部得分
                comments_count_province = {"安徽": 0, "澳门": 0, "北京": 0, "福建": 0, "甘肃": 0, "广东": 0, "广西": 0,
                                           "贵州": 0, "海南": 0, "河北": 0, "河南": 0, "黑龙江": 0, "湖北": 0, "湖南": 0,
                                           "吉林": 0, "江苏": 0, "江西": 0, "辽宁": 0, "内蒙古": 0, "宁夏": 0, "青海": 0,
                                           "山东": 0, "山西": 0, "陕西": 0, "上海": 0, "四川": 0, "台湾": 0, "天津": 0,
                                           "西藏": 0, "香港": 0, "新疆": 0, "云南": 0, "浙江": 0, "重庆": 0, "海外": 0,
                                           "其他": 0, }
                comments = []
                see_comments_num = 0
                for fc in new_communication_map_data[ori_data[i][0]]['data']:
                    if fc['C_F'] == 'C':
                        comments.append(fc)
                        see_comments_num += 1

                if see_comments_num:
                    for co in comments:
                        if co['fc_user']['province'] in comments_count_province.keys():
                            comments_count_province[co['fc_user']['province']] = 1
                    for j in alpha_province:
                        influence += alpha[3] * alpha_province[j] * comments_count_province[j]

                        #     print(influence)

                # 转发局部得分
                see_forwards_num = 0
                if "rank1_num" in self.info[ori_data[i][0]].keys():
                    forwards_count_province = {"安徽": 0, "澳门": 0, "北京": 0, "福建": 0, "甘肃": 0, "广东": 0, "广西": 0,
                                               "贵州": 0, "海南": 0, "河北": 0, "河南": 0, "黑龙江": 0, "湖北": 0, "湖南": 0,
                                               "吉林": 0, "江苏": 0, "江西": 0, "辽宁": 0, "内蒙古": 0, "宁夏": 0, "青海": 0,
                                               "山东": 0, "山西": 0, "陕西": 0, "上海": 0, "四川": 0, "台湾": 0, "天津": 0,
                                               "西藏": 0, "香港": 0, "新疆": 0, "云南": 0, "浙江": 0, "重庆": 0, "海外": 0,
                                               "其他": 0, }
                    forward = [self.info[ori_data[i][0]]["data"]["children"][j] for j in
                               range(self.info[ori_data[i][0]]["rank1_num"])]
                    for k in forward:
                        if k["children"] != []:
                            for l in k["children"]:
                                if l not in forward:
                                    forward.append(l)
                    see_forwards_num = len(forward)

                    for fo in forward:
                        if fo['user']:
                            if fo['user']['province'] in forwards_count_province.keys():
                                forwards_count_province[fo['user']['province']] = 1

                    for j in alpha_province:
                        influence += alpha[5] * alpha_province[j] * forwards_count_province[j]

                        #     print(see_comments_num, see_forwards_num)
                #     print(influence)
                #     print("==============================")
                self.info[ori_data[i][0]]["influence"] = influence

        def add_key_words():
            for data in self.info:
                if "rank1_num" in self.info[data].keys():
                    sentence = []
                    temp = [self.info[data]["data"]["children"][j] for j in
                            range(self.info[data]["rank1_num"])]
                    for k in temp:
                        if k["children"] != []:
                            for l in k["children"]:
                                if l not in temp:
                                    temp.append(l)
                    for j in temp:
                        if j["value"] != '':
                            sentence.append(j["value"])

                    sentence = participle(sentence)

                    if sentence != []:
                        words = tfidf(sentence)

                        for j in temp:
                            j["key_words"] = []
                            flag = 0
                            for k in words:
                                if k in j["value"]:
                                    j["key_words"].append(k)
                                    flag += 1
                                    if flag >= 3:
                                        break

        def calculation(forward, rank, father):
            forward_1 = []
            for j in forward:
                if j[1].count("//@") == rank - 1:
                    forward_1.append(j)
                    father.append(
                        {"name": j[0], "user": forward_user_info[j[0]] if j[0] in forward_user_info.keys() else '',
                         "value": j[1].split(":")[-1], "forward_id": j[3], "children": []})
            forward_without_1 = [j for j in forward if j not in forward_1]

            # print(forward_without_1)

            for j in father:
                if j["user"]:
                    _id = j["user"]["id"]
                    name = ""
                    for k in forward_1:
                        if k[0] == _id:
                            name = "//@" + k[1]
                            break
                    # print("new_name:", name)
                    if len(k[1].split(":")) > 1:
                        forward2 = [k for k in forward_without_1 if name in k[1]]
                        if forward2 != []:
                            for l in range(len(forward2)):
                                forward2[l][1] = forward2[l][1].replace(name, "")
                            # print(forward2)
                            calculation(forward2, 1, j["children"])

        for i in ori_data:
            self.info[i[0]] = {}
            self.info[i[0]]["content"] = i[2]
            self.info[i[0]]["content_id"] = i[0]
            self.info[i[0]]["user"] = user_info[i[1]]
            self.info[i[0]]["emotion"] = emotion[i[0]] if i[0] in emotion.keys() else ""
            self.info[i[0]]["pics"] = 1 if i[8] or i[9] else 0
            self.info[i[0]]["topic"] = topic[i[0]] if i[0] in topic.keys() else ""
            if i[0] in forward_info.keys():
                forward = forward_info[i[0]]
                # print(forward)
                self.info[i[0]]["forward_num"] = len(forward)

                rank_num = 0
                for j in forward:
                    if j[1].count("//@") > rank_num:
                        rank_num = j[1].count("//@")

                rank = [0 for _ in range(rank_num + 2)]

                for j in forward:
                    rank[j[1].count("//@")] += 1

                # print(rank)
                for j in range(len(rank)):
                    if rank[j] == 0:
                        self.info[i[0]]["rank_num"] = j
                        break
                    else:
                        self.info[i[0]]["rank" + str(j + 1) + "_num"] = rank[j]

                if "rank_num" in self.info[i[0]].keys():
                    self.info[i[0]]["data"] = {"name": i[0], "value": i[2], "children": []}

                    forward_1 = []
                    for j in forward:
                        if j[1].count("//@") == 0:
                            forward_1.append(j)
                            self.info[i[0]]["data"]["children"].append(
                                {"name": j[0], "user": forward_user_info[j[0]] if j[
                                                                                      0] in forward_user_info.keys() else '',
                                 "value": j[1].split(":")[-1], "forward_id": j[3], "children": []})
                    if self.info[i[0]]["rank_num"] > 1:
                        # print(forward_1)
                        forward_without_1 = [j for j in forward if j not in forward_1]
                        # print(forward_without_1)
                        for j in self.info[i[0]]["data"]["children"]:
                            if j["user"]:
                                _id = j["user"]["id"]
                                for k in forward_1:
                                    if k[0] == _id:
                                        name = "//@" + k[1]
                                        break
                                # print(name)
                                if 1 < len(name.split(":")):
                                    forward2 = []
                                    for k in forward_without_1:
                                        if name in k[1]:
                                            forward2.append(k)
                                    # print(forward2)
                                    if forward2:
                                        for l in range(len(forward2)):
                                            forward2[l][1] = forward2[l][1].replace(name, "")
                                        # print(forward2)
                                        calculation(forward2, 1, j["children"])
                else:
                    self.info[i[0]]["rank_num"] = 0

        add_key_words()
        add_influence()
        low_dimensional_coordinate = DataDimensionReduction().calculate(ori_data, user_info)
        for i in self.info:
            self.info[i]["coordinate"] = low_dimensional_coordinate[i]

        print("CommunicationMap ready!!")
        return self.info


class Overview:
    """
    用于生成overview数据

    传入参数类简介：
    ori_data:list

    users_info:dict,

    time:dict

    topic:dict,

    返回参数简介：
    self.map2time:dict,
                    键值为地点（用户信息中的provence），
                    值类型list，
                    存储微博发布时间，微博内容id

    self.time2topic:dict
                    键值为时间，
                    值类型dict，
                    存储每个主题下微博数量和对应id
    """

    def __init__(self):
        self.map2time = {}
        self.time2topic = {}

    def creat(self, ori_data, users_info, time, topic):
        temp = []
        for i in range(len(ori_data)):
            temp.append([ori_data[i][0], users_info[ori_data[i][1]]["province"], time[ori_data[i][0]].split(" ")[0]])
        for i in temp:
            if i[1] not in self.map2time.keys():
                self.map2time[i[1]] = []
            self.map2time[i[1]].append([i[-1], i[0]])

        temp = []
        temp_dict = {}
        for i in range(len(ori_data)):
            temp.append([ori_data[i][0], time[ori_data[i][0]].split(" ")[0], topic[ori_data[i][0]]["topic"]])
        for i in temp:
            if i[1] not in temp_dict.keys():
                temp_dict[i[1]] = {}
            if i[2] not in temp_dict[i[1]].keys():
                temp_dict[i[1]][i[2]] = {"num": 0, "id": []}
            temp_dict[i[1]][i[2]]["num"] += 1
            temp_dict[i[1]][i[2]]["id"].append(i[0])

        for i in temp_dict:
            self.time2topic[i] = {"date": i, "topic": []}
            for j in temp_dict[i]:
                self.time2topic[i]["topic"].append({"name": j,
                                                    "num": temp_dict[i][j]["num"],
                                                    "id": temp_dict[i][j]["id"]
                                                    })

        print("Overview ready!!")
        return self.map2time, self.time2topic


class Middlelevel:
    """
    用于生成middlelevel数据

    传入参数类简介：
    ori_data:list

    time:dict

    topic:dict,

    emotion:dict,

    influence:dict

    返回参数简介：
    self.circle:dict,
                键值为微博内容id，
                值为dict，
                存储发布时间，情感，主题，长度，影响力信息
    """

    def __init__(self):
        self.circle = {}

    def creat(self, ori_data, time, topic, emotion, influence):
        temp = []
        for i in range(len(ori_data)):
            temp.append([ori_data[i][0], time[ori_data[i][0]].split(" ")[0],
                         topic[ori_data[i][0]]["topic"], emotion[ori_data[i][0]], len(ori_data[i][2]),
                         int(influence[ori_data[i][0]]["repost"]) * 0.5 + int(
                             influence[ori_data[i][0]]["comment"]) * 0.3 + int(influence[ori_data[i][0]]["like"]) * 0.2
                         ])
        for i in temp:
            self.circle[i[0]] = {"time": i[1], "topic": i[2], "emotion": i[3], "length": i[4], "influence": i[5]}

        print("Middlelevel ready!!")
        return self.circle


class NewCommunicationMap(object):
    """
    传入参数简介：
        介绍略，参考其他地方

    返回参数简介：
        self.info:dict,
                键值为微博内容id,
                内容为id，内容，发表时间，用户信息，情感信息，评论信息
    """

    def __init__(self):
        self.info = {}

    def creat(self, ori_data, time, users_info, emotion, fc2020, commentusers, forward_users_info, fcemotion):
        for i in ori_data:
            self.info[i[0]] = {
                "content_id": i[0],
                "content": i[-1],
                "created_at": time[i[0]],
                "user_info": users_info[i[1]],
                "emotion": emotion[i[0]],
                "data": []}
            for j in fc2020:
                if j[0] == i[0] and (j[1] in commentusers.keys() or j[1] in forward_users_info.keys()):
                    self.info[i[0]]["data"].append(
                        {"fc_user": commentusers[j[1]] if j[1] in commentusers.keys() else forward_users_info[j[1]],
                         "content": j[2], "created_at": j[3], "like_num": j[4], "C_F": j[5],
                         "emotion": fcemotion[j[6]]})
        return self.info


class DataDimensionReduction(object):
    """
    计算谣言的降维坐标

    传入参数简介：
        ori_data:list
        users_info:dict

    返回参数简介：
        self.high_dimensional_info:list
            存储谣言高维特征依次分别为：发布用户粉丝数，发布用户关注数，发布用户微博数，发布用户信息完整度，微博转发数，微博评论数，微博点赞数，
            微博长度，微博内容含有图片或视频链接数量
        self.low_dimensional_coordinate:dict
                键值为微博内容id,
                内容为低维坐标
    """

    def __init__(self):
        self.high_dimensional_info = []
        self.low_dimensional_coordinate = {}

    def calculate(self, ori_data, users_info):

        for i in ori_data:
            count = 0
            self.high_dimensional_info.append([int(users_info[i[1]]['fans_num']), int(users_info[i[1]]['follows_num']),
                                               int(users_info[i[1]]['tweets_num'])])
            for j in users_info[i[1]]:
                if users_info[i[1]][j] is not None:
                    count += 1
            self.high_dimensional_info[-1].append(count)
            self.high_dimensional_info[-1].append(int(i[5]))
            self.high_dimensional_info[-1].append(int(i[3]))
            self.high_dimensional_info[-1].append(int(i[4]))
            self.high_dimensional_info[-1].append(len(i[2]))
            if i[8] is not None and i[9] is not None:
                self.high_dimensional_info[-1].append(2)
            elif i[8] is not None or i[9] is not None:
                self.high_dimensional_info[-1].append(1)
            else:
                self.high_dimensional_info[-1].append(0)

        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
        X_tsne = tsne.fit_transform(np.array(self.high_dimensional_info))

        for i in range(len(self.high_dimensional_info)):
            self.low_dimensional_coordinate[ori_data[i][0]] = [str(X_tsne[i][0]), str(X_tsne[i][1])]
        return self.low_dimensional_coordinate


class TreeMap(object):
    """
    用于生成树状图数据

    传入参数类简介：
    ori_data:list

    user_info:dict,

    forward_info:dict，

    forward_users_info:dict,

    emotion:dict,

    返回参数简介：
    self.info:dict
            键值为微博内容id，
            值为dict，存储传播链上各种信息

    """

    def __init__(self):
        self.info = {}

    def creat(self, ori_data: list, user_info: dict, forward_info: dict, forward_user_info: dict, emotion: dict,
              fcemotion: dict, temp_data: dict):
        for i in ori_data[:]:
            self.info[i[0]] = []
            self.info[i[0]].append({"content_id": i[0], "content": i[2],
                                    "emotion": int(emotion[i[0]]["value"]) if i[0] in emotion.keys() else "",
                                    "user": user_info[i[1]], "level": 0, "words_num": len(i[2]),
                                    "influence": temp_data[i[0]]["influence"]})

            if "rank1_num" in temp_data[i[0]].keys():
                forward = [temp_data[i[0]]["data"]["children"][j] for j in range(temp_data[i[0]]["rank1_num"])]
                for k in forward:
                    if k["children"] != []:
                        for l in k["children"]:
                            if l not in forward:
                                forward.append(l)
                for k in forward:
                    for j in forward_info[i[0]]:
                        if j[3] == k['forward_id']:
                            femotion = int(fcemotion[k['forward_id']]) - 1 if k['forward_id'] in fcemotion.keys() else 0

                            self.info[i[0]].append({"content": k["value"], "created_at": j[2],
                                                    "words_num": len(k["value"]),
                                                    "user": forward_user_info[j[0]] if j[0] in forward_user_info.keys()
                                                    else '',
                                                    "level": j[1].count("//@") + 1, 'forward_id': j[3],
                                                    "emotion": femotion,
                                                    "key_words": k['key_words'] if 'key_words' in k.keys() else ""})
        return self.info


class NewTreeMap():
    def __init__(self):
        self.info = {}
        self.comment_kes_words = ["假的", "假了", "编的", "假消息", "假新闻", "造谣", "传谣", "谣言", "不实", "虚假", "伪造", "澄清"]

    def creat(self, ori_data: list, users_info: dict, forward_info: dict, forward_users_info: dict, emotion: dict,
              fcemotion: dict, temp_data: dict, fc2020: list):
        for i in ori_data[:]:
            self.info[i[0]] = {}
            self.info[i[0]][i[0]] = {"content_id": i[0], "full_content": i[2], "created_at": i[7],
                                     "emotion": int(emotion[i[0]]["value"]) if i[0] in emotion.keys() else "",
                                     "user": users_info[i[1]], "level": 0, "words_num": len(i[2]),
                                     "influence": temp_data[i[0]]["influence"], "son": []}

            self.info[i[0]]["comments"] = {}
            for j in fc2020:
                if j[0] == i[0] and j[5] == "C" and j[2] is not None and not isinstance(j[2], float):
                    key_words = []
                    for k in self.comment_kes_words:
                        if k in j[2]:
                            key_words.append(k)
                    self.info[i[0]]["comments"][j[6]] = {"only_id": j[6], "content": j[2], "created_at": j[3],
                                                         "emotion": int(fcemotion[j[6]]) - 1 if j[6] in fcemotion.keys() and fcemotion[j[6]] != 'nan'
                                                         else 0, "key_words": copy.deepcopy(key_words)}

            if i[0] in forward_info.keys():
                all_level_forward_content = set()
                max_level = 0
                for k in forward_info[i[0]]:
                    all_level_forward_content.add(k[1])
                    if k[1].count("//@") > max_level:
                        max_level = k[1].count("//@")

                level_content = [set() for _ in range(max_level + 1)]
                son = {}
                for j in all_level_forward_content:
                    md5 = hashlib.md5()
                    md5.update(j.encode("utf8"))
                    hashid = md5.hexdigest()
                    if hashid not in son.keys():
                        son[hashid] = []
                    level_count = j.count("//@")
                    level_content[level_count].add(j)

                    this_hashid = copy.deepcopy(hashid)
                    thislevel_content = copy.deepcopy(j)
                    for k in range(level_count - 1, -1, -1):
                        if thislevel_content.find("//@") != -1:
                            last_content = copy.deepcopy(thislevel_content)[thislevel_content.find("//@") + 3:]

                            md5 = hashlib.md5()
                            md5.update(last_content.encode("utf8"))
                            last_hashid = md5.hexdigest()

                            if last_hashid not in son.keys():
                                son[last_hashid] = []

                            level_content[k].add(last_content)
                            thislevel_content = copy.deepcopy(last_content)

                            son[last_hashid].append(this_hashid)
                            this_hashid = copy.deepcopy(last_hashid)

                        elif thislevel_content != '':
                            last_content = copy.deepcopy(thislevel_content)
                            level_content[k].add(last_content)
                            break
                for j in level_content:
                    j.discard('')
                for j in range(len(level_content)):
                    for k in level_content[j]:
                        flag = 0
                        md5 = hashlib.md5()
                        md5.update(k.encode("utf8"))
                        hashid = md5.hexdigest()
                        for l in forward_info[i[0]]:
                            if k == l[1]:
                                flag = 1
                                if j == 0:
                                    part_content = copy.deepcopy(k)[k.find(":") + 1:]
                                else:
                                    part_content = copy.deepcopy(k)[k.find(":") + 1:k.find("//@")]
                                femotion = int(fcemotion[l[3]]) - 1 if l[3] in fcemotion.keys() else 0
                                self.info[i[0]][hashid] = {"full_content": k, "content": part_content, "key_words": [],
                                                           "created_at": l[2], "words_num": len(k),
                                                           "user": forward_users_info[l[0]] if l[
                                                                                                   0] in forward_users_info.keys() else '',
                                                           "level": j + 1, 'forward_id': hashid, "emotion": femotion,
                                                           "son": son[hashid]}
                                break
                        if flag == 0:
                            if j == 0:
                                part_content = copy.deepcopy(k)[k.find(":") + 1:]
                            else:
                                part_content = copy.deepcopy(k)[k.find(":") + 1:k.find("//@")]
                            self.info[i[0]][hashid] = {"full_content": k, "content": part_content, "key_words": [],
                                                       "created_at": '', "words_num": len(k), "user": '',
                                                       "level": j + 1,
                                                       'forward_id': hashid, "emotion": '', "son": son[hashid]}
                sentence = []
                for j in self.info[i[0]]:
                    if "level" in self.info[i[0]][j].keys():
                        if self.info[i[0]][j]["level"] == 1:
                            self.info[i[0]][i[0]]["son"].append(self.info[i[0]][j]['forward_id'])
                        if "content" in self.info[i[0]][j].keys():
                            sentence.append(copy.deepcopy(self.info[i[0]][j]["content"]))

                sentence = participle(sentence)

                if sentence:
                    words = tfidf(sentence)

                    for j in self.info[i[0]]:
                        if "level" in self.info[i[0]][j].keys():
                            if "content" in self.info[i[0]][j].keys():
                                flag = 0
                                if "谣" in self.info[i[0]][j]["content"]:
                                    self.info[i[0]][j]["key_words"].append("谣")
                                if "假" in self.info[i[0]][j]["content"]:
                                    self.info[i[0]][j]["key_words"].append("假")
                                if "标题党" in self.info[i[0]][j]["content"]:
                                    self.info[i[0]][j]["key_words"].append("标题党")
                                if "没毛病" in self.info[i[0]][j]["content"]:
                                    self.info[i[0]][j]["key_words"].append("没毛病")
                                for k in words:
                                    if k in self.info[i[0]][j]["content"] and k not in ["原本", "事情", "单方面", "工作",
                                                                                        "总结", "代码", "事儿", "专门", "亲戚",
                                                                                        "恶心", "毛病", "犊子", "东西", "重要性",
                                                                                        "无脑", "代表", "公证处", "工作人员",
                                                                                        "原则", "公证处"]:
                                        self.info[i[0]][j]["key_words"].append(k)
                                        flag += 1
                                        if flag >= 3:
                                            break
        return self.info
