import requests
import json
from datetime import datetime
import time
from tools import find_playing_show


class Amagi_commander():
    def __init__(self, base_url, token, feed_code, show_id=None):
        self.base_url = base_url
        self.show_id = show_id
        self.token = token
        self.feed_code = feed_code

    def set_show_id(self, show_id):
        self.show_id = show_id
    def set_token(self, token):
        self.token = token
    def set_feed_code(self, feed_code):
        self.feed_code = feed_code
    
    def update_show_id_from_live_playlist(self):
        show = find_playing_show(self.base_url, self.token)
        if show:
            self.set_show_id(show)
            print(f"Updated show_id to: {self.show_id}")
        else:
            print("No show is currently airing.")

    def action(self, action_name="take_next", take_type="segment", epoch=int(time.time())*1000, log=False):

        if self.show_id is None:
            print("ERRO: show_id nao definido. Use set_show_id() para definir.")
            return
        
        url = f"{self.base_url}/api/v2/shows/{self.show_id}/playout/actions?token={self.token}"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.token}",
        }
        payload = {
            "show_id": self.show_id,
            "action_name": action_name,
            "epoch": epoch,
            "feed_code": self.feed_code,
            "take_type": take_type,
        }

        if log:
            print(f"Fazendo requisição para: {url}")
            print(f"Payload: {payload}\n")

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if log:
                print(f"Status: {response.status_code}")
                print(f"Resposta: {data}")
            
        except requests.exceptions.ConnectionError:
            print("ERRO: Nao conseguiu conectar ao servidor.")
            print("Verifique se a aplicacao esta rodando em http://localhost:5000")
            
        except requests.exceptions.RequestException as e:
            print(f"ERRO: {e}")
            
        except json.JSONDecodeError:
            print("ERRO: Resposta nao eh um JSON valido")
            print(f"Resposta: {response.text}")

        except Exception as e:
            print(f"ERRO inesperado: {e}")

