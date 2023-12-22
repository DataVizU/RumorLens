import json
import copy
from typing import List

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

from src.data_process.get_data_local import GetData
from src.data_process.dataprocess import (
    CommunicationMap,
    Overview,
    Middlelevel,
    NewCommunicationMap,
    NewTreeMap,
    flow_kew_words,
)

(
    ori_data,
    time,
    influence,
    users_info,
    forward_info,
    forward_users_info,
    emotion,
    topic,
    commentusers,
    fc2020,
    fcemotion,
) = GetData(
    "src/database"
).creat()  # 初始化读取数据库信息

(
    copy_ori_data,
    copy_time,
    copy_influence,
    copy_users_info,
    copy_forward_info,
    copy_forward_users_info,
    copy_emotion,
    copy_topic,
    copy_commentusers,
    copy_fc2020,
    copy_fcemotion,
) = (
    copy.deepcopy(ori_data),
    copy.deepcopy(time),
    copy.deepcopy(influence),
    copy.deepcopy(users_info),
    copy.deepcopy(forward_info),
    copy.deepcopy(forward_users_info),
    copy.deepcopy(emotion),
    copy.deepcopy(topic),
    copy.deepcopy(commentusers),
    copy.deepcopy(fc2020),
    copy.deepcopy(fcemotion),
)

overview_data = Overview().creat(ori_data, users_info, time, topic)
middle_level_data = Middlelevel().creat(ori_data, time, topic, emotion, influence)

dimension_reduction_data = CommunicationMap().creat(
    ori_data,
    users_info,
    forward_info,
    forward_users_info,
    emotion,
    time,
    fc2020,
    commentusers,
    fcemotion,
    topic,
)

tree_map_data = NewTreeMap().creat(
    copy_ori_data,
    copy_users_info,
    copy_forward_info,
    copy_forward_users_info,
    copy_emotion,
    copy_fcemotion,
    dimension_reduction_data,
    copy_fc2020,
)

ids = []
for i in ori_data:
    ids.append(i[0])
ftk = flow_kew_words(ids, ori_data, copy_topic)

new_communication_map_data = NewCommunicationMap().creat(
    ori_data,
    time,
    users_info,
    emotion,
    fc2020,
    commentusers,
    forward_users_info,
    fcemotion,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/overview/{data_type}")
async def get_overview(data_type: str):
    result = {}
    if overview_data:
        if data_type == "time2topic":
            result = json.dumps(overview_data[1], ensure_ascii=False)
        elif data_type == "map2time":
            result = json.dumps(overview_data[0], ensure_ascii=False)

    return result


@app.post("/overview/theme-river")
async def get_river_data(content_id: List[str] = Body(...)):
    content_ids = content_id
    key_words = {}
    if content_ids:
        key_words = flow_kew_words(content_ids, ori_data, copy_topic)

    return key_words


@app.post("/middle")
async def get_middle_level(content_id: List[str] = Body(...)):
    result = []
    if dimension_reduction_data:
        for data in content_id:
            content_id_dict = {'content_id': data}
            target_dict = dimension_reduction_data.get(data)
            if target_dict:
                content_id_dict.update(target_dict)
            result.append(content_id_dict)

    return result


@app.get("/communication/{content_id}")
async def get_communication_map(content_id: str):
    result = {}
    if new_communication_map_data:
        result = new_communication_map_data.get(content_id)

    return result


@app.get("/spiral/{content_id}")
async def get_spiral_map(content_id: str):
    result = {}
    if new_communication_map_data:
        result = new_communication_map_data.get(content_id)

    return result


@app.get("/treemap/{content_id}")
async def get_tree_map(content_id: str):
    result = []
    if tree_map_data:
        result = tree_map_data.get(content_id)

    return result
