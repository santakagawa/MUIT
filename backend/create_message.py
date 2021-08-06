import json


def create_mission_message(name: str, level: int, image: str, contents: str):

    message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": image,
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "gravity": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "position": "absolute",
                    "background": {
                        "type": "linearGradient",
                        "angle": "0deg",
                        "endColor": "#00000000",
                        "startColor": "#00000099"
                    },
                    "width": "100%",
                    "height": "40%",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": name,
                                            "size": "lg",
                                            "color": "#DD3311",
                                            "weight": "bold",
                                            "style": "normal"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "難易度" + str(level),
                                            "color": "#EE2222",
                                            "offsetEnd": "none",
                                            "margin": "none",
                                            "flex": 0
                                        },
                                    ],
                                    "spacing": "xs"
                                },
                                {
                                    "type": "text",
                                    "text": contents,
                                    "color": "#FF3321"
                                }
                            ],
                            "spacing": "xs"
                        }
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "paddingAll": "20px",
                    "background": {
                        "type": "linearGradient",
                        "angle": "30deg",
                        "startColor": "#111111EE",
                        "endColor": "#ffffff00"
                    }
                }
            ],
            "paddingAll": "0px"
        }
	}
	
    left_star = {
        "type": "icon",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
        "margin": "xxl"
    }
    
    star = {
        "type": "icon",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    }

    diasble_star = {
        "type": "icon",
        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
    }

    for i in range(6):
        
        if level > i:
            if i==0:
                img = left_star
            else:
                img = star
        else:
            img = diasble_star
        
        message['body']['contents'][2]['contents'][0]['contents'][1]['contents'].append(img)

    return message

def create_congrats_message(point: int):

    message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "ポイント獲得",
                "color": "#299ae6",
                "weight": "bold"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "https://previews.123rf.com/images/ylivdesign/ylivdesign1902/ylivdesign190207842/125008365-dollar-coin-icon-isometric-of-dollar-coin-vector-icon-for-web-design-isolated-on-white-background.jpg",
                    "size": "45px",
                    "align": "start",
                    "flex": 0,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": str(point),
                    "gravity": "center",
                    "weight": "bold",
                    "size": "3xl",
                    "margin": "lg",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": "ポイント",
                    "gravity": "center",
                    "weight": "bold",
                    "margin": "sm"
                }
                ],
                "paddingTop": "lg",
                "paddingBottom": "md"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "🎉おめでとうございます🎉\n\nあなたは完璧にミッションを達成されました！💯💯\n\n報酬として、Primeポイントを受け取ってください！\n\n次のミッションも頑張りましょう✨",
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

    return message

def create_procedure_message(text_list,progress_list,contents_list):
    # text_listは手順の名前
    # progresslistは進捗度・"70％"などの文字列
    # contentlistは手順の説明
    message = {
        "type": "carousel",
        "contents": []
    }
    for i in range(len(text_list)):
        text = text_list[i]
        progress = progress_list[i]
        contents = contents_list[i]
        new_contents = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": text,
                    "color": "#ffffff",
                    "align": "start",
                    "size": "md",
                    "gravity": "center"
                },
                {
                    "type": "text",
                    "text": progress,
                    "color": "#ffffff",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
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
                            "type": "filler"
                        }
                        ],
                        "width": progress,
                        "backgroundColor": "#FE5658",
                        "height": "6px"
                    }
                    ],
                    "backgroundColor": "#9FD8E36E",
                    "height": "6px",
                    "margin": "sm"
                }
                ],
                "backgroundColor": "#44AAFD",
                "paddingTop": "19px",
                "paddingAll": "12px",
                "paddingBottom": "16px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": contents,
                        "color": "#8C8C8C",
                        "size": "sm",
                        "wrap": True
                    }
                    ],
                    "flex": 1
                }
                ],
                "spacing": "md",
                "paddingAll": "12px"
            },
            "styles": {
                "footer": {
                "separator": False
                }
            }
            }
        message['contents'].append(new_contents)

    return message


def create_failure_message():
    message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ミッション失敗",
                        "color": "#299ae6",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [],
                        "paddingTop": "lg",
                        "paddingBottom": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "おおっとミッションに失敗してしまったようデス....😨😨 \n\nもう一度手順をよく読んで再チャレンジしてみましょう！！",
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
    
    return message