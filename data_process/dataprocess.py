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

    def creat(self, ori_data: list, user_info: dict, forward_info: dict, forward_user_info: dict, emotion: dict):
        global name

        def calculation(forward, rank, father):
            forward_1 = []
            for j in forward:
                if j[1].count("//@") == rank - 1:
                    forward_1.append(j)
                    father.append(
                        {"name": j[0], "user": forward_user_info[j[0]] if j[0] in forward_user_info.keys() else '',
                         "value": j[1].split(":")[-1], "children": []})
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

        for i in ori_data[:]:
            self.info[i[0]] = {}
            self.info[i[0]]["content"] = i[2]
            self.info[i[0]]["content_id"] = i[0]
            self.info[i[0]]["user"] = user_info[i[1]]
            self.info[i[0]]["emotion"] = emotion[i[0]] if i[0] in emotion.keys() else ""
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
                                 "value": j[1].split(":")[-1], "children": []})
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
