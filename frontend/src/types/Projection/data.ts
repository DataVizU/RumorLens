export interface Data {
  content: string;
  content_id: string;
  coordinate: number[];
  data: {
    children: Children[];
    name: string;
    value: string;
  };
  emotion: {
    negative_prob: number;
    positive_prob: number;
    value: number;
  };
  forward_num: number;
  influence: number;
  pics: number;
  rank1_num: number;
  rank2_num: number;
  rank3_num: number;
  rank_num: number;
  topic: {
    topic: string;
    prob: number;
  };
  user: User;
}

export interface User {
  authentication: string;
  birthday: string;
  brief_introduction: string;
  city: string;
  fans_num: number;
  follows_num: number;
  gender: string;
  id: number;
  labels: string;
  nike_name: string;
  province: string;
  tweets_num: number;
  vip_level: string;
}

export interface Children {
  children: Children[];
  forward_id: string;
  key_words: string[];
  name: string;
  user: User;
  value: string;
}
