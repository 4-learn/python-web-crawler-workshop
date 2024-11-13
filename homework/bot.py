from linebot import LineBotApi
from linebot.models import TextSendMessage

line_bot_api = LineBotApi('arjFaYSIko0DltLyFb1EDbfUlx8000vNL0XD6KGQsGkNM5/uQL5GhaB+9D+J6TpcuozluKK7V95Qb/RvjJ1EXwu7+WttmFoM2vZbTbrapDBoHgMWiogW4Dxep4zeKhVFnN0Hg2yQrv/qtXZnKeDrjwdB04t89/1O/w1cDnyilFU=')

def send_line_notification(message):
    line_bot_api.push_message('yillkid', TextSendMessage(text=message))
