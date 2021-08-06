import os
import json
from urllib import request
import boto3
import logging

import create_message

# ロガー作成
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DBインスタンス作成
dynamodb = boto3.resource('dynamodb')

# テーブルの定義
user_table = dynamodb.Table('intern-groupa-user')
group_table = dynamodb.Table('intern-groupa-group')

############## 以下に処理を記述 ##############

text_list = [
    "第1ステップ",
    "第2ステップ",
    "第3ステップ"
]

progress_list = [
    "33%",
    "66%",
    "100%"
]

contents_list = [
    "画面左下のカメラボタン📷を押す",
    "カメラが起動、撮影ボタンを押す",
    "送信ボタンを押す"
]

def check_stamp(event):
    event_type = event['events'][0]['type']
    if event_type != 'message':
        # 返信内容は仮
        messages = [
            {
                "type":"flex",
                "altText": "mission message",
                "contents":create_message.create_failure_message()
            }
        ]
        return messages
        
    message_type = event['events'][0]['message']['type']
    if message_type == 'sticker':
        # 返信内容
        messages = [
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_congrats_message(30)
            },
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_mission_message("ミッション2", 2, "https://everydayicons.jp/wp/wp-content/themes/everydayicons/icons/thumbs/ei-picture.png", "📷 画像を送信してみましょう📷")
            },
            {
                "type": "flex",
                "altText": "mission procedure",
                "contents": create_message.create_procedure_message(text_list, progress_list, contents_list)
            }
        ]
        # mission_idを更新
        group_id = event['events'][0]['source']['groupId']
        group_table.update_item(
            Key={'id': group_id},
            UpdateExpression="set mission=:m",
            ExpressionAttributeValues={
                ':m': '2'
            }
        )
        # pointを更新
        target_id = group_table.get_item(Key={'id': group_id})['Item']['target']
        point = int(user_table.get_item(Key={'id': target_id})['Item']['point'])
        user_table.update_item(
            Key={'id': target_id},
            UpdateExpression="set point=:p",
            ExpressionAttributeValues={':p': str(point + 100)}
            )
    else:
        messages = [
            {
                "type":"flex",
                "altText": "mission message",
                "contents":create_message.create_failure_message()
            }
        ]
    return messages