import os
import json
from urllib import request
import boto3
import logging
import create_message
from check_registration import get_user_name

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
    "第3ステップ",
    "第4ステップ",
    "第5ステップ",
]

progress_list = [
    "20%",
    "40%",
    "60%",
    "80%",
    "100%",
]

contents_list = [
    "入力画面の右端にある笑顔😊のマークを押す",
    "送りたいスタンプを選択する",
    "そのスタンプを押す。",
    "プレビューが表示されるので、ちゃんと送りたいものか、確認する。",
    "もう一度押して送信完了"
]

def check_playing_start(event):
    event_text = event['events'][0]['message']['text']
    if event_text == '始めます':
        # 返信内容は仮
        messages = [
            {
                "type":"text",
                "text":"ミッションを開始します"
            },
            {
            	"type": "flex",
            	"altText": "mission message",
            	"contents": create_message.create_mission_message("ミッション1", 1, "https://renote.jp/files/blobs/proxy/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBcFZTIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--f38b550ff470c8ca991c91d62ac5974ffa33561b/20150529_780425.jpg", "😊スタンプを送ってみよう😊")
            },
            {
                "type": "flex",
                "altText": "mission procedure",
                "contents": create_message.create_procedure_message(text_list, progress_list, contents_list)
            }
        ]

        #playingをTrueに変更して開始
        group_id = event['events'][0]['source']['groupId']
        group_table.update_item(
            Key={'id': group_id},
            UpdateExpression="set playing=:m",
            ExpressionAttributeValues={
                ':m': True
            }
        )
        return messages
        
    else:
        # 返信内容は仮
        messages = [
            {
                "type":"text",
                "text":"ミッションを開始するには「始めます」とコメントしてください"
            }
        ]
    return messages