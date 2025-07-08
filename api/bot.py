import os
import requests
from bs4 import BeautifulSoup
from telebot import TeleBot
from dotenv import load_dotenv

# Enviroment load
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://dreamerscast.com/home/release/432-dandadan-2nd-season"

bot = TeleBot(TOKEN)

def get_episodes():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    playlist = soup.find(id="player_playlist1")
    episodes = []

    if playlist:
        items = playlist.find_all("div")

        for i in items:
            text = i.get_text(strip=True)
            if text and text not in episodes:
                episodes.append(text)
    return episodes

def handler(request):
    episodes = get_episodes()
    
    for e in episodes:
        msg = f"Новая серия **Dan Da Dan** вышла в твоей любимой озвучке **[DreamCast]({URL})**"
        bot.send_message(CHAT_ID, msg)
    return {"Status": "ok", "sent": len(episodes)}