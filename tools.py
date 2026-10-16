import requests
import json
import time
from datetime import datetime, timedelta, timezone


def get_show_id_by_name(base_url, token, show_name):
    
    try:    
        data = get_shows(base_url, token)
        if not data:
            return None
        for show in data:
            if show.get("name") == show_name:
                return show.get("show_id")
        
        print(f"Show '{show_name}' not found.")
        return None
    except requests.exceptions.ConnectionError:
        print("ERRO: Nao conseguiu conectar ao servidor.")

def is_show_currently_airing(show):
    start_time = show.get("start_time")
    end_time = show.get("end_time")
    if not start_time or not end_time:
        return False

    now = datetime.now(timezone.utc)
    start = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
    return start <= now < end


def find_playing_show(base_url, token):
    shows = find_shows_in_live_playlist(base_url, token)
    for show in shows:
        if is_show_currently_airing(show):
            return show.get("show_id")

def find_shows_in_live_playlist(base_url, token):
    live_playlist = find_live_playlist(base_url, token)
    if not live_playlist:
        return None
    show_ids = live_playlist.get("show_ids")
    shows_ = get_shows(base_url, token)

    #print(f"Show IDs from live playlist: {show_ids}")  # Debugging line to check the show IDs
    #print(f"Shows retrieved: {shows_}")  # Debugging line to check the shows data
    shows = [show for show in shows_ if show.get("id") in show_ids]
    #print(shows)
    return shows


def get_shows(base_url, token):

    url = f"{base_url}/api/v2/shows?token={token}"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.json()
         
    except requests.exceptions.ConnectionError:
        print("ERRO: Nao conseguiu conectar ao servidor.")

def find_live_playlist(base_url, token, feed_id = 2):
    """https://bandnews.cloudport.amagi.tv/v1/api/playlist.json?feed_id=2&start_date=2026-09-25&state=published&ptype=normal"""
    date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"{base_url}/v1/api/playlist.json?token={token}&feed_id={feed_id}&start_date={date}&state=published&ptype=normal"
    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        #print(f"Data received: {data}")  # Debugging line to check the response data
        
        for playlist in data.get("playlists"):
            #print(f"Checking playlist: {playlist}")  # Debugging line to check each playlist
            if playlist.get("is_playing") == True:
                return playlist
        
        print(f"Live playlist not found.")
        return None
    except requests.exceptions.ConnectionError:
        print("ERRO: Nao conseguiu conectar ao servidor.")
