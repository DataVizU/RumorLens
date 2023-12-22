import pandas as pd


class GetData:

    def __init__(self, databasePath):
        self.databasePath = databasePath
        self.ori_data = []
        self.time = {}
        self.influence = {}
        self.users_info = {}
        self.forward_info = {}
        self.forward_users_info = {}
        self.commentusers = {}
        self.fc2020 = []
        self.fcemotion = {}
        self.emotion = {}
        self.topic = {}

    def creat(self):
        texts_data = pd.read_csv(f'{self.databasePath}/texts2020.csv', na_values='NaN')
        texts_data = texts_data.fillna("nan")
        for _, row in texts_data.iterrows():
            self.ori_data.append(
                [str(row["_id"]), str(row["user_id"]), row["content"], row["comment_num"], row["like_num"],
                 row["repost_num"], row["crawl_time"], row["created_at"], row["image_url"],
                 row["video_url"], row["weibo_url"], row["origin_weibo"]])
            self.time[str(row["_id"])] = row["created_at"]
            self.influence[str(row["_id"])] = {"repost": row["repost_num"], "comment": row["comment_num"],
                                               "like": row["like_num"]}

        users_data = pd.read_csv(f'{self.databasePath}/users2020.csv', na_values='NaN')
        users_data = users_data.fillna("nan")
        for _, row in users_data.iterrows():
            self.users_info[str(row["_id"])] = {
                'id': str(row["_id"]),
                'nick_name': row["nick_name"],
                'authentication': row["authentication"],
                'birthday': row["birthday"],
                'brief_introduction': row["brief_introduction"],
                'city': row["city"],
                'fans_num': row["fans_num"],
                'follows_num': row["follows_num"],
                'gender': row["gender"],
                'labels': row["labels"],
                'province': row["province"],
                'tweets_num': row["tweets_num"],
                'vip_level': row["vip_level"]
            }

        commentusers_data = pd.read_csv(f'{self.databasePath}/commentusers2020.csv', na_values='NaN')
        commentusers_data = commentusers_data.fillna("nan")
        for _, row in commentusers_data.iterrows():
            self.commentusers[str(row["_id"])] = {
                'id': str(row["_id"]),
                'authentication': row["authentication"],
                'birthday': row["birthday"],
                'brief_introduction': row["brief_introduction"],
                'city': row["city"],
                'fans_num': row["fans_num"],
                'follows_num': row["follows_num"],
                'gender': row["gender"],
                'labels': row["labels"],
                'province': row["province"],
                'sentiment': row["sentiment"],
                'sex_orientation': row["sex_orientation"],
                'tweets_num': row["tweets_num"],
                'vip_level': row["vip_level"]
            }

        forwardusers_data = pd.read_csv(f'{self.databasePath}/forwardusers2020.csv', na_values='NaN')
        forwardusers_data = forwardusers_data.fillna("nan")
        for _, row in forwardusers_data.iterrows():
            self.forward_users_info[str(row["_id"])] = {
                'id': str(row["_id"]),
                'nick_name': row["nick_name"],
                'authentication': row["authentication"],
                'birthday': row["birthday"],
                'brief_introduction': row["brief_introduction"],
                'city': row["city"],
                'fans_num': row["fans_num"],
                'follows_num': row["follows_num"],
                'gender': row["gender"],
                'labels': row["labels"],
                'province': row["province"],
                'tweets_num': row["tweets_num"],
                'vip_level': row["vip_level"]
            }

        fc2020_data = pd.read_csv(f'{self.databasePath}/fc2020.csv', na_values='NaN')
        fc2020_data = fc2020_data.fillna("nan")
        for _, row in fc2020_data.iterrows():
            self.fc2020.append([str(row["weibo_id"]), str(row["fc_user_id"]), row["content"],
                                row["created_at"], row["like_num"], row["C_F"], str(row["only_id"])])

        emotion_data = pd.read_csv(f'{self.databasePath}/emotion.csv', na_values='NaN')
        emotion_data = emotion_data.fillna("nan")
        for _, row in emotion_data.iterrows():
            self.emotion[str(row["id"])] = {"value": row["emotion"],
                                       'positive_prob': row["positive_prob"],
                                       'negative_prob': row["negative_prob"]
                                       }

        fcemotion_data = pd.read_csv(f'{self.databasePath}/fcemotion.csv', na_values='NaN')
        fcemotion_data = fcemotion_data.fillna("nan")
        for _, row in fcemotion_data.iterrows():
            self.fcemotion[str(row["only_id"])] = row["label"]

        topic_data = pd.read_csv(f'{self.databasePath}/topic.csv', na_values='NaN')
        topic_data = topic_data.fillna("nan")
        for _, row in topic_data.iterrows():
            self.topic[str(row["id"])] = {"topic": row["topic"], "prob": row["prob"]}

        forwards_data = pd.read_csv(f'{self.databasePath}/forwards2020.csv', na_values='NaN')
        forwards_data = forwards_data.fillna("nan")
        for _, row in forwards_data.iterrows():
            if str(row["weibo_id"]) not in self.forward_info.keys():
                self.forward_info[str(row["weibo_id"])] = []
            self.forward_info[str(row["weibo_id"])].append(
                [str(row["forward_user_id"]), row["content"], row["created_at"], str(row["_id"])])

        print(len(self.ori_data), len(self.time), len(self.influence), len(self.users_info), len(self.forward_info),
              len(self.forward_users_info), len(self.emotion), len(self.topic), len(self.commentusers),
              len(self.fc2020), len(self.fcemotion))

        return self.ori_data, self.time, self.influence, self.users_info, self.forward_info, self.forward_users_info, \
            self.emotion, self.topic, self.commentusers, self.fc2020, self.fcemotion
