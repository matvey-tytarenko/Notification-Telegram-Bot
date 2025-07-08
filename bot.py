import os
from dotenv import load_dotenv
from parser_inspect import URL
import telebot
import requests
from bs4 import BeautifulSoup

# ENV FILE
load_dotenv()

BOT_API = os.getenv("TOKEN")
bot = telebot.TeleBot(BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    text = (f"Привет {message.from_user.username} Я бот оповещалка который будет оповещать о новых эпизодах Аниме Dan Da Dan в озвучке **[Dream Cast]({URL})**"
            )
    bot.reply_to(message, text, parse_mode="Markdown")

def manual_check(message):
    episodes = get_episodes()
    if episodes:
        send_notification(episodes)
        bot.send_message(message, f"**Вышла новая серия --> [смотреть]({URL})**", parse_mode="Markdown")
    else:
        return

def get_episodes():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        playlist = soup.find(id="player_playlist1")

        episodes = []
        if playlist:
            for i in playlist.find_all("div"):
                text = i.get_text(strip=True)
                if text and text not in episodes:
                    episodes.append(text)
        return episodes 
    except Exception as e:
        print(f"[ERROR] get_episodes: {e}")
        return []

def send_notification(episodes, message):
    for e in episodes:
        msg = f"Новая серия **Dan Da Dan 2** ---> {e} [смотреть]({URL})"
        try:
            bot.send_message(message, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"[Error] send_message: {e}")

if __name__ == '__main__':
    bot.polling(non_stop=True)