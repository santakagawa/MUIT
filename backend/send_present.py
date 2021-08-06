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

def send_present(event):
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
    if message_type == 'image':
        # 返信内容は仮
        messages = [
            {
            	"type": "flex",
            	"altText": "flex_message",
            	"contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "image",
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "1:1",
                            "gravity": "center",
                            "url": "https://lh3.googleusercontent.com/proxy/I07VQK9ztRANoFlgYg_fEVPPRJW-VSeS85RArtEqJGuOQPJoHeqMTvnJf9o6PAC7SZ5Mv8JxIC-3f23v4eywxa2_ZqczKnpC7MPg5wzdMOaonryY0ORqOSVwZuIFn_wmJPGGFDKu-dEw6QBv6HkREoyOdORBMTNmWtc9Jz_raiycd5db0r2s0g4"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "全ミッション達成",
                                    "weight": "bold",
                                    "color": "#299ae6"
                                }
                                ],
                                "position": "absolute",
                                "paddingAll": "xxl"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "🎉おめでとうございマス🎉\n\n全ミッション達成デス！\n\nまた分からなくなったときは、私を呼んでくださいネ🤖🤖",
                                        "wrap": True,
                                        "gravity": "bottom",
                                        "size": "17px",
                                        "margin": "none",
                                        "offsetTop": "none",
                                        "offsetBottom": "none"
                                    }
                                    ],
                                    "borderWidth": "none",
                                    "cornerRadius": "xl",
                                    "backgroundColor": "#edf2fa",
                                    "paddingAll": "xl"
                                }
                                ],
                                "paddingAll": "xxl",
                                "offsetTop": "40px",
                                "height": "300px"
                            }
                            ],
                            "position": "absolute",
                            "background": {
                            "type": "linearGradient",
                            "angle": "0deg",
                            "startColor": "#ffffff00",
                            "endColor": "#f2f2f2CC"
                            }
                        }
                        ],
                        "paddingAll": "none",
                        "height": "270px"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": "#299ae6"
                    }
                    }
            }
        ]
        # mission_idを更新(次のミッションのために1に)
        group_id = event['events'][0]['source']['groupId']
        group_table.update_item(
            Key={'id': group_id},
            UpdateExpression="set mission=:m",
            ExpressionAttributeValues={
                ':m': '1'
            }
        )
        # pointを更新(暫定的にミッションが終了したら０ポイントに変更)
        target_id = group_table.get_item(Key={'id': group_id})['Item']['target']
        user_table.update_item(
            Key={'id': target_id},
            UpdateExpression="set point=:p",
            ExpressionAttributeValues={':p': "0"}
            )
        # playing終了
        group_table.update_item(
            Key={'id': group_id},
            UpdateExpression="set playing=:m",
            ExpressionAttributeValues={
                ':m': False
            }
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