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
    "画面左下にあるプラスボタン➕を押す",
    "画面の下側にメニューが出てくるので、「位置情報」ボタンを押す",
    "現在位置のマップが表示されるので、「この位置を送信」ボタンを押す"
]

def check_cancel(event):
    event_type = event['events'][0]['type']
    if event_type != 'unsend':
        # 返信内容は仮
        messages = [
            {
                "type":"flex",
                "altText": "mission message",
                "contents":create_message.create_failure_message()
            }
        ]
        return messages

    else:
        # 返信内容は仮
        messages = [
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_congrats_message(30)
            },
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_mission_message("ミッション5", 5, "https://dekiru.net/upload_docs/img/20180606_o0204.png", "📍位置情報を送信してみましょう📍")
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
                ':m': '5'
            }
        )
        # pointを更新
        target_id = group_table.get_item(Key={'id': group_id})['Item']['target']
        point = int(user_table.get_item(Key={'id': target_id})['Item']['point'])
        user_table.update_item(
            Key={'id': target_id},
            UpdateExpression="set point=:p",
            ExpressionAttributeValues={':p': str(point + 30)}
            )
    return messages