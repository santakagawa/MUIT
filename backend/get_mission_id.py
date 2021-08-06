import os
import json
from urllib import request
import boto3
import logging

# ロガー作成
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DBインスタンス作成
dynamodb = boto3.resource('dynamodb')

# テーブルの定義
user_table = dynamodb.Table('intern-groupa-user')
group_table = dynamodb.Table('intern-groupa-group')

############## 以下に処理を記述 ##############

# 進行中のミッションIDを取得(進行中でなければFalseを返す)
def get_mission_id(event):
    
    group_id = event['events'][0]['source']['groupId']
    group_resp = group_table.get_item(Key={'id': group_id})['Item']
    playing = group_resp['playing']

    # ミッションが進行中の場合
    if playing:
        mission_id = group_resp['mission']
    else:
        mission_id = False
    
    return mission_id
