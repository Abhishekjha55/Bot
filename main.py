import requests
import telebot
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from flask import Flask

Flask app for Keep Alive

app = Flask(name)

@app.route('/')
def home():
return "Bot is Alive!"

def run_flask():
app.run(host='0.0.0.0', port=8080)

Bot Token

BOT_TOKEN = '7686518024:AAHmfmQVjfFLbR4Ea-85nVTXogNPQex11CA'
bot = telebot.TeleBot(BOT_TOKEN)

Channel IDs

PRIVATE_CHANNEL_IDS = ['-1002176694831', '-1001953658822', '-1002364212227']
PUBLIC_CHANNEL_ID = '@EARNEREARN'

Image URLs

BIG_IMAGE_URL = 'https://i.imgur.com/epJUzLi.jpeg'
SMALL_IMAGE_URL = 'https://i.imgur.com/JOHjW7t.jpeg'

Links for Private Channel

PRIVATE_REGISTER_LINK = 'https://www.6diuwin.com/#/register?invitationCode=55424154169'

Links for Public Channel

PUBLIC_REGISTER_LINK = 'https://www.6diuwin.com/#/register?invitationCode=63716150187'

Common Fund Management Link

FUND_MANAGEMENT_LINK = 'https://t.me/EARNEREARN/2355'

Function to generate Period Number (1 Step Ahead)

def generate_period_number():
future_time = datetime.now() + timedelta(minutes=1)
minutes_since_midnight = (future_time.hour * 60) + future_time.minute
period_number = future_time.strftime('%Y%m%d') + f'{minutes_since_midnight:04d}'
return period_number

Function to extract trend from website

def get_trend():
url = 'https://5diuwi .com/#/home/AllLotteryGames/WinGo?id=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

trend_text = soup.find('div', class_='trend-class').text.strip()

if 'BIG' in trend_text.upper():
return 'BIG'
elif 'SMALL' in trend_text.upper():
return 'SMALL'
else:
return random.choice(['BIG', 'SMALL'])

Function to check result from website

def check_result(period_number):
url = f'https://5diuwi .com/#/home/AllLotteryGames/WinGo?id=1&period={period_number}'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

result_text = soup.find('div', class_='result-class').text.strip()

if 'BIG' in result_text.upper():
return 'WIN'
elif 'SMALL' in result_text.upper():
return 'LOSS'
else:
return 'Result Pending'

Function to send prediction message

def send_prediction():
period_number = generate_period_number()
prediction = get_trend()
image_url = BIG_IMAGE_URL if prediction == "BIG" else SMALL_IMAGE_URL

caption = f"""

<b>🎯 Prediction Alert 🎯</b>

🕒 <b>Period:</b> <code>{period_number}</code>
📊 <b>Prediction:</b> <b>{prediction}</b>
🟠 <b>Result:</b> <b>Result Pending...</b>

<b>WINGO 1 MIN</b>
"""

Sending to Private Channels
messages = []
for channel_id in PRIVATE_CHANNEL_IDS:
private_markup = telebot.types.InlineKeyboardMarkup()
private_markup.add(
telebot.types.InlineKeyboardButton("📈 Fund Management", url=FUND_MANAGEMENT_LINK),
telebot.types.InlineKeyboardButton("📝 Register", url=PRIVATE_REGISTER_LINK)
)

message = bot.send_photo(channel_id, image_url, caption=caption, parse_mode='HTML', reply_markup=private_markup)  
messages.append((channel_id, message.message_id))
Sending to Public Channel
public_markup = telebot.types.InlineKeyboardMarkup()
public_markup.add(
telebot.types.InlineKeyboardButton("📈 Fund Management", url=FUND_MANAGEMENT_LINK),
telebot.types.InlineKeyboardButton("📝 Register", url=PUBLIC_REGISTER_LINK)
)

message = bot.send_photo(PUBLIC_CHANNEL_ID, image_url, caption=caption, parse_mode='HTML', reply_markup=public_markup)
messages.append((PUBLIC_CHANNEL_ID, message.message_id))

Result Update Logic
time.sleep(60)
result = check_result(period_number)
updated_caption = caption.replace("Result Pending...", result)

Updating Result in All Channels
for channel_id, message_id in messages:
bot.edit_message_caption(updated_caption, channel_id, message_id, parse_mode='HTML')

Function to send prediction at the start of every minute (no delays)

def schedule_prediction():
while True:
current_time = datetime.now()
current_second = current_time.second
sleep_time = 60 - current_second

time.sleep(sleep_time)
send_prediction()

Run the bot and Flask server simultaneously

import threading
threading.Thread(target=run_flask).start()
schedule_prediction()