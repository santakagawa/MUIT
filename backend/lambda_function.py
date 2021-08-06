import json
import os
import boto3
from urllib import request
import logging

# ロギングの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DBインスタンス作成
dynamodb = boto3.resource('dynamodb')

# テーブルの定義
user_table = dynamodb.Table('intern-groupa-user')
group_table = dynamodb.Table('intern-groupa-group')

# ファイルの読み込み
import check_registration, get_mission_id, check_stamp, check_image, check_mention, check_cancel, check_location, send_present, check_playing_start, create_message

def lambda_handler(event, context):
  logger.info(event)  
  # リクエストヘッダー
  req_headers = {
      'Authorization': 'Bearer ' + os.environ['LINE_CHANNEL_ACCESS_TOKEN'],
      'Content-Type': 'application/json'
  }
  
  if event['events'][0]['type'] == 'join':
    messages = [
        {
                "type":"flex",
                "altText": "welcome message",
                "contents":{
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://img.freepik.com/free-vector/bot-chat-say-hi-robots-that-are-programmed-talk-customers-online_68708-622.jpg?size=626&ext=jpg",
                        "size": "4xl",
                        "aspectRatio": "20:17",
                        "aspectMode": "cover",
                        "action": {
                        "type": "uri",
                        "uri": "http://linecorp.com/"
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "はじめまして！ 私はPrimeJapan（プライムジャパン）です😃\n\nLINEの使い方に慣れるお手伝いをさせていただきます☺️☺️  \n\n LINEでできることを紹介していきますので、一緒に試してみましょう！\n\n  成功すると、おトクに使えるポイントがもらえます✨",
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
                            "margin": "none",
                            "backgroundColor": "#edf2fa",
                            "paddingAll": "xl"
                        }
                        ],
                        "borderWidth": "none",
                        "margin": "none"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": []
                    },
                    "styles": {
                        "footer": {
                        "backgroundColor": "#299ae6"
                        }
                    }
                }
            },
            {
            "type":"text",
            "text":"「登録します」とコメントしてユーザー登録をしてください"
            }
    ]
    logger.info(messages)

    req_body = {
        'replyToken': event['events'][0]['replyToken'],
        'messages': messages
        }

    req = request.Request(
        'https://api.line.me/v2/bot/message/reply',
        json.dumps(req_body).encode('utf-8'),
        method='POST',
        headers=req_headers
        )

    # リクエスト送信
    with request.urlopen(req, timeout=10) as res:
        pass
  elif event['events'][0]['type'] == 'message' and ('text' in event['events'][0]['message']) and event['events'][0]['message']['text'] == 'ポイント確認':
    
    user_id = event['events'][0]['source']['userId']
    user_name = check_registration.get_user_name(user_id)
    
    try:
        user_resp = user_table.get_item(Key={'id': user_id})['Item']
        user_point = user_resp['point']
    except:
        user_point = "0"
    
    messages = [
        {
            "type": "flex",
            "altText": "welcome message",
            "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ポイント詳細",
                                "color": "#299ae6",
                                "weight": "bold",
                                "margin": "none"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "【" + user_name +  "さんの現在の所有ポイント】",
                                        "wrap": True,
                                        "gravity": "bottom",
                                        "size": "17px",
                                        "margin": "none",
                                        "offsetTop": "none",
                                        "offsetBottom": "none"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": user_point,
                                                "gravity": "center",
                                                "weight": "bold",
                                                "size": "4xl",
                                                "margin": "none",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": "ポイント",
                                                "gravity": "center",
                                                "weight": "bold",
                                                "margin": "sm",
                                                "size": "lg"
                                            }
                                        ],
                                        "paddingTop": "lg",
                                        "paddingBottom": "md"
                                    },
                                    {
                                        "type": "text",
                                        "text": "\nポイントがたまったら、\nギフトに交換してみマショウ🎁",
                                        "wrap": True
                                    }
                                ],
                                "borderWidth": "none",
                                "cornerRadius": "xl",
                                "margin": "md",
                                "backgroundColor": "#edf2fa",
                                "paddingAll": "xl"
                            }
                        ],
                        "borderWidth": "none",
                        "margin": "none"
                    },
                "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": []
                        },
                "styles": {
                        "footer": {
                            "backgroundColor": "#299ae6"
                        }
                        }
            }
        }
    ]
    logger.info(messages)

    req_body = {
        'replyToken': event['events'][0]['replyToken'],
        'messages': messages
        }

    req = request.Request(
        'https://api.line.me/v2/bot/message/reply',
        json.dumps(req_body).encode('utf-8'),
        method='POST',
        headers=req_headers
        )

    # リクエスト送信
    with request.urlopen(req, timeout=10) as res:
        pass
      
  
  try:
    registration_flg = check_registration.check_registration(event)
  except:
    registration_flg = False
  
  if registration_flg:
    
      # 進行中のミッションがあるか(返り値: 進行中のミッションID or False)
      mission_id = get_mission_id.get_mission_id(event)

      # 各ミッションに対応する関数(返り値: レスポンスボディ)
      if mission_id:
          if mission_id == '1':
              messages = check_stamp.check_stamp(event)
          elif mission_id == '2':
              messages = check_image.check_image(event)
          elif mission_id == '3':
              messages = check_mention.check_mention(event)
          elif mission_id == '4':
              messages = check_cancel.check_cancel(event)
          elif mission_id == '5':
              messages = check_location.check_location(event)
          elif mission_id == '6':
              messages = send_present.send_present(event)
      #　暫定的に「始めます」に反応してplayingをTrueに
      else:
        messages = check_playing_start.check_playing_start(event)
              
      logger.info(messages)
      # リクエストボディ
      # 送信取り消しにはreplyTokenがないため場合分け
      if mission_id == '4' or mission_id == '5':
        req_body = {
            'messages': messages,
            'to': event['events'][0]['source']['groupId']
        }
        req = request.Request(
            'https://api.line.me/v2/bot/message/push',
            json.dumps(req_body).encode('utf-8'),
            method='POST',
            headers=req_headers
        )
      
      else:
        req_body = {
            'replyToken': event['events'][0]['replyToken'],
            'messages': messages
        }
        
        req = request.Request(
            'https://api.line.me/v2/bot/message/reply',
            json.dumps(req_body).encode('utf-8'),
            method='POST',
            headers=req_headers
        )
      
      # リクエスト送信
      with request.urlopen(req, timeout=10) as res:
        pass
    
  return 0