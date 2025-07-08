import requests
from bs4 import BeautifulSoup

URL = "https://dreamerscast.com/home/release/432-dandadan-2nd-season"

def check_dandadan():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    playlist = soup.find(id="player_playlist1")
    if playlist:
        episodes = playlist.find_all(string="event")

        for ep in episodes:
            print("Event detected: {ep.strip()}")
    else:
        print("Episodes not found!")