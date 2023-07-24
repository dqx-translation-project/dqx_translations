import os
import requests


WEBLATE_HOST = os.environ["WEBLATE_HOST"]
WEBLATE_API_TOKEN = os.environ["WEBLATE_API_TOKEN"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


headers = {
    "Authorization": f"Token {WEBLATE_API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(f"{WEBLATE_HOST}/api/projects/dqx/statistics/", headers=headers)
num_suggestions = response.json()["suggestions"]

if num_suggestions != 0:
    message = f"There are currently {num_suggestions} suggestion(s) pending review. Check Weblate for more details."
    data = { "content": message, "username": "Weblate" }
    requests.post(url=DISCORD_WEBHOOK_URL, data=data)
