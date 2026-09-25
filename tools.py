import requests
import json


def get_show_id_by_name(base_url, token, show_name):
    url = f"{base_url}/api/v2/shows?token={token}"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for show in data:
            if show.get("name") == show_name:
                return show.get("show_id")
        
        print(f"Show '{show_name}' not found.")
        return None
    except requests.exceptions.ConnectionError:
        print("ERRO: Nao conseguiu conectar ao servidor.")