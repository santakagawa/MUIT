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
    "取り消したいメッセージを長押しする",
    "メニューが出てくるので、「送信取り消し」ボタンを押す",
    "確認画面が出てくるので、「取り消す」ボタンを押す"
]

def check_mention(event):
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

    if 'mention' in event['events'][0]['message']:
        # 返信内容は仮
        messages = [
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_congrats_message(50)
            },
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_mission_message("ミッション4", 4, "https://t14.pimg.jp/047/497/814/1/47497814.jpg", "❌送信を取り消してみましょう❌")
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
                ':m': '4'
            }
        )
        # pointを更新
        target_id = group_table.get_item(Key={'id': group_id})['Item']['target']
        point = int(user_table.get_item(Key={'id': target_id})['Item']['point'])
        user_table.update_item(
            Key={'id': target_id},
            UpdateExpression="set point=:p",
            ExpressionAttributeValues={':p': str(point + 50)}
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