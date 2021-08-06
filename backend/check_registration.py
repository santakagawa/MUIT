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

# ユーザIDからユーザ名を取得する関数
def get_user_name(user_id):

  # リクエストURL
  req_url = 'https://api.line.me/v2/bot/profile/' + user_id
  
  # ヘッダー
  req_headers = {
    'Authorization': 'Bearer ' + os.environ['LINE_CHANNEL_ACCESS_TOKEN']
  }

  # リクエストオブジェクトを作成
  req = request.Request(req_url, headers=req_headers)

  # ユーザ名を取得
  with request.urlopen(req) as res:
    res_body = json.loads(res.read().decode('UTF-8'))
    user_name = res_body['displayName']
  
  return user_name

# ユーザが登録済みかを返却
def check_registration(event):

    # イベントソースタイプを取得(個人 or グループ)
    source_type = event['events'][0]['source']['type']
        
    # グループの場合
    if source_type == 'group':
        
        # グループID, ユーザIDの取得
        user_id = event['events'][0]['source']['userId']
        group_id = event['events'][0]['source']['groupId']
        
        # グループ情報取得
        try:
            group_resp = group_table.get_item(Key={'id': group_id})['Item']
            logger.info(group_resp)
            target_id = group_resp['target']
            # ユーザがターゲットユーザであった時
            if target_id == user_id:
                return True
    
        # グループがDBに存在しなかった場合
        except:
            
            try:
                user_resp = user_table.get_item(Key={'id': user_id})['Item']
                logger.info(user_resp)

            # ユーザ情報が存在しなかった場合
            except:
                
                event_text = ''
                
                if 'text' in event['events'][0]['message']:
                    # メッセージを取得
                    event_text = event['events'][0]['message']['text']
                    
                # メッセージが'登録します'だった場合
                if event_text == '登録します':
                    # 送信元ユーザをミッション対象ユーザとして登録
                    group_table.put_item(Item={
                        'id': group_id,
                        'target': user_id,
                        'mission': '1',
                        'playing': False
                    })
                
                    # ユーザ情報をDBに登録
                    user_table.put_item(Item={
                        'id': user_id,
                        'group': group_id,
                        'name': get_user_name(user_id),
                        'point': '0'
                    })
                    
                    messages = [
                        {
                            "type": "text",
                            "text": get_user_name(user_id)+ "さんを対象ユーザとして登録しました"
                        },
                        {
                            "type":"text",
                            "text":"ミッションを開始するには「始めます」とコメントしてください"
                        }   
                    ]
                    
                    req_body = {
                        'replyToken': event['events'][0]['replyToken'],
                        'messages': messages
                    }
                    
                    req_headers = {
                        'Authorization': 'Bearer ' + os.environ['LINE_CHANNEL_ACCESS_TOKEN'],
                        'Content-Type': 'application/json'
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
                    
        return False