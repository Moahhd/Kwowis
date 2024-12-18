import os
import re
import random
import string
from base64 import b64decode
import requests
import sys
import time
from datetime import datetime
from requests import get
from time import sleep
from random import choice, randint
from fake_useragent import UserAgent
from telethon import TelegramClient, sync, errors, types, functions
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.sessions import StringSession
from config import session_string, api_id, api_hash

# بيانات البوت
BOT_TOKEN = "7935545001:AAFkUH5dRPTAkCqkDksrcrZr8xcfa44s6N0"
USER_ID = 6838671491  # المعرف الخاص بك

# رابط الفيديو المطلوب
VIDEO_URL = "https://t.me/cc_king_the/1446"

class ChackUserName:
    def __init__(self, ses):
        self.Client = ses
        self.names = set()
        self.generate_username()

    def user_gen(self):
        """توليد أسماء المستخدمين من النمط Vip0000 إلى Vip10000"""
        for i in range(10000):  # تكرار حتى 10000
            yield f"Vip{i:04d}"  # توليد الأسماء بالنمط Vip0000, Vip0001, ...

    def generate_username(self):
        numb = 0
        usernames = self.user_gen()  # استدعاء الدالة لتوليد الأسماء
        for user in usernames:
            if user.lower() not in self.names:
                self.names.add(user.lower())
                try:
                    Fragment = self.Chack_UserName_Fragment(user)
                except:
                    self.names.discard(user)
                    continue
                numb += 1
                if Fragment == "taken":
                    print(f"-[{numb}] UserName is Taken [@{user}]")
                elif Fragment == "available":
                    print(f"-[{numb}] UserName is Sold [@{user}]")
                elif Fragment == "Unavailable":
                    print(f"-[{numb}] UserName is Unavailable [@{user}]")
                    self.Chack_UserName_TeleGram(user, numb)
                elif Fragment == "unknown":
                    print(f"-[{numb}] UserName is unknown [@{user}]")
                    self.names.discard(user)
                else:
                    print(f"-[{numb}] Error is [{Fragment}]")

    def Chack_UserName_TeleGram(self, user, numb):
        try:
            tele = self.Client(CheckUsernameRequest(username=user))
            if tele:
                print(f"- UserName is Good (CheckUsernameRequest) [{user}]")
                # إرسال إلى البوت عبر API
                current_time = datetime.now().strftime("%I:%M")
                message = f'''❲ 𝖋𝖑𝖔𝖔𝖉 ❳ ⌯ @{user}\n❲ {current_time} ❳ ⌯ @patatavip
 ❲ 𝖈𝖑𝖎𝖈𝖐 ❳  ⌯ {numb}'''
                self.send_message_to_bot(message)
            else:
                print(f"- UserName is Bad (CheckUsernameRequest) [{user}] Taken.")
        except errors.rpcbaseerrors.BadRequestError:
            print(f"- UserName is Band [@{user}]")
            return
        except errors.FloodWaitError as timer:
            num = int(timer.seconds)
            print(f"- Error Account Flood (CheckUsernameRequest) Time [{num}]\n- UserName [{user}]\n")
            while num > 0:
                print(f"The flood will end after: [{num}]", end="\r")
                time.sleep(0.00)
                num -= 1
            self.names.discard(user)
            return
        except errors.UsernameInvalidError:
            print(f"- UserName is Invalid [@{user}]")
            return

    def send_message_to_bot(self, message):
        """إرسال رسالة إلى البوت باستخدام Telegram Bot API."""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": USER_ID,
            "text": message
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("- Message sent successfully to bot.")
                # إرسال الفيديو مع الكليشة
                video_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
                video_data = {
                    "chat_id": USER_ID,
                    "video": VIDEO_URL,
                    "caption": message  # الكليشة مرفقة مع الفيديو
                }
                video_response = requests.post(video_url, data=video_data)
                if video_response.status_code == 200:
                    print("- Video sent successfully to bot.")
                else:
                    print(f"- Failed to send video: {video_response.status_code}, {video_response.text}")
            else:
                print(f"- Failed to send message: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"- Error sending message: {e}")

    def Chack_UserName_Fragment(self, user):
        try:
            response = requests.get(f"https://fragment.com/username/{user}", timeout=15).text
            if '<span class="tm-section-header-status tm-status-taken">Taken</span>' in response:
                return "taken"
            elif '<span class="tm-section-header-status tm-status-unavail">Sold</span>' in response:
                return "available"
            elif '<div class="table-cell-status-thin thin-only tm-status-unavail">Unavailable</div>' in response:
                return "Unavailable"
            else:
                return "unknown"
        except Exception as e:
            return e

if __name__ == "__main__":
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
    client.start()
    ChackUserName(client)
