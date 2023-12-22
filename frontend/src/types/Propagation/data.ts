import type { User } from "@/types/Projection/data";

export interface RawData {
  [key: string]: RawDataValue;
}

export interface RawDataValue {
  content: string;
  created_at: string;
  createTime: number;
  emotion: string;
  forward_id: string;
  full_content: string;
  key_words: string[];
  level: number;
  son: string[];
  user: User;
  words_num: number;
}

export interface LevelData {
  [key: string]: RawData;
}

export interface TimeData {
  [key: string]: TimeDataValue; // key是level
}

export interface TimeDataValue {
  [key: string]: TimeDataValueValue; // key是时间
}

export interface TimeDataValueValue {
  name: string;
  sum: number;
  children: TimeDataValueValueChild[];
}

export interface TimeDataValueValueChild {
  name: string;
  size: number;
  son: string[];
  level: number;
}

export interface RawTimeLineData {
  [key: string]: string[];
}

export interface TimeLineData {
  [key: string]: number;
}

export interface ListData {
  ID: string;
  data: RawDataValue;
}

export interface DetailData {
  "Full Content": string;
  "Create Time": string;
  userDetail: {
    id: number;
    Authentication: string;
    Gender: string;
    "Fans Number": number | string;
    "Follows Number": number | string;
    "Tweets Number": number | string;
    "VIP Level": string;
  };
}
