import pymongo


class Database:

    def __init__(self, mongo_url, name):
        print("Connecting to Database..." + name)
        self.conn = pymongo.MongoClient(mongo_url)
        self.db = self.conn[name]
        print("Connected to db :)")

    def get_state(self):
        return self.conn is not None and self.db is not None


class GetData:
    """
    返回参数简介：
    self.ori_data：list
            每个元素也为一个list，
            存储：微博内容及相关信息

    self.time:dict
            键值为用户id，
            存储每条信息的发布时间，

    self.influence:dict
            键值为用户id，
            值类型为dict，
            存储转评赞信息，

    self.user_info:dict,
            键值为用户id，
            值类型为dict，
            存储用户信息

    self.forward_info：dict，
                键值为微博内容id，
                值类型为list，存储参与转发的信息（长度为2，类型为str）

    self.forward_users_info:dict,
                    键值为用户id，
                    值类型为dict，
                    存储用户信息

    self.emotion:dict,
            键值为微博内容id，
            值类型为dict，
            存储情感信息

    self.topic:dict,
            键值为微博内容id，
            值类型为dict，
            存储情感信息

    self.commentusers:dict,
                    键值为用户id，
                    值类型为dict，
                    存储用户信息

    self.fc2020:list,
            每个元素也为一个list（长度为7， 类型均为str），
            存储：微博内容id，用户id和内容，发布时间，点赞数，转发或评论类型，内容唯一id,

    self.fcemotion:dict,
                    键值为内容唯一id,
                    内容为情感标签，
    """

    def __init__(self, url):
        self.url = url
        self.ori_data = []
        self.time = {}
        self.influence = {}
        self.users_info = {}
        self.forward_info = {}
        self.forward_users_info = {}
        self.emotion = {}
        self.topic = {}
        self.commentusers = {}
        self.fc2020 = []
        self.fcemotion = {}

    def creat(self):
        odclient = Database(self.url, "texts")
        odcollection = odclient.db["texts2020"]
        for data in odcollection.find():
            self.ori_data.append([data["_id"], data["user_id"], data["content"], data["comment_num"], data["like_num"],
                                  data["repost_num"], data["crawl_time"], data["created_at"], data["image_url"],
                                  data["video_url"], data["weibo_url"], data["origin_weibo"]])
            self.time[data["_id"]] = data["created_at"]
            self.influence[data["_id"]] = {"repost": data["repost_num"], "comment": data["comment_num"],
                                           "like": data["like_num"]}

        odcollection2 = odclient.db["fc2020"]
        for data in odcollection2.find():
            self.fc2020.append([data["weibo_id"], data["fc_user_id"], data["content"],
                                data["created_at"], data["like_num"], data["C_F"], data["only_id"]])

        uiclient = Database(self.url, "users")
        uicollection = uiclient.db["users2020"]
        for data in uicollection.find():
            self.users_info[data["_id"]] = {
                'id': data["_id"],
                'nick_name': data["nick_name"],
                'authentication': data["authentication"],
                'birthday': data["birthday"],
                'brief_introduction': data["brief_introduction"],
                'city': data["city"],
                'fans_num': data["fans_num"],
                'follows_num': data["follows_num"],
                'gender': data["gender"],
                'labels': data["labels"],
                'province': data["province"],
                'tweets_num': data["tweets_num"],
                'vip_level': data["vip_level"]
            }

        uicollection2 = uiclient.db["commentusers2020"]
        for data in uicollection2.find():
            self.commentusers[data["_id"]] = {
                'id': data["_id"],
                'authentication': data["authentication"],
                'birthday': data["birthday"],
                'brief_introduction': data["brief_introduction"],
                'city': data["city"],
                'fans_num': data["fans_num"],
                'follows_num': data["follows_num"],
                'gender': data["gender"],
                'labels': data["labels"],
                'province': data["province"],
                'sentiment': data["sentiment"],
                'sex_orientation': data["sex_orientation"],
                'tweets_num': data["tweets_num"],
                'vip_level': data["vip_level"]
            }

        fuiclient = Database(self.url, "forwardusers")
        fuicollection = fuiclient.db["forwardusers2020"]
        for data in fuicollection.find():
            self.forward_users_info[data["_id"]] = {
                'id': data["_id"],
                'nick_name': data["nick_name"],
                'authentication': data["authentication"],
                'birthday': data["birthday"],
                'brief_introduction': data["brief_introduction"],
                'city': data["city"],
                'fans_num': data["fans_num"],
                'follows_num': data["follows_num"],
                'gender': data["gender"],
                'labels': data["labels"],
                'province': data["province"],
                'tweets_num': data["tweets_num"],
                'vip_level': data["vip_level"]
            }

        fclient = Database(self.url, "forwards")
        fcollection = fclient.db["forwards2020"]
        for data in fcollection.find():
            if data["weibo_id"] not in self.forward_info.keys():
                self.forward_info[data["weibo_id"]] = []
            self.forward_info[data["weibo_id"]].append([data["forward_user_id"], data["content"]])

        eclient = Database(self.url, "emotion")
        ecollection = eclient.db["emotion"]
        for data in ecollection.find():
            self.emotion[data["id"]] = {"value": data["emotion"],
                                        'positive_prob': data["positive_prob"],
                                        'negative_prob': data["negative_prob"]
                                        }

        ecollection2 = eclient.db["fcemotion"]
        for data in ecollection2.find():
            self.fcemotion[data["only_id"]] = data["label"]

        tclient = Database(self.url, "topic")
        tcollection = tclient.db["topic"]
        for data in tcollection.find():
            self.topic[data["id"]] = {"topic": data["topic"], "prob": data["prob"]}

        return self.ori_data, self.time, self.influence, self.users_info, self.forward_info, self.forward_users_info, \
               self.emotion, self.topic, self.commentusers, self.fc2020, self.fcemotion
