from dotenv import load_dotenv
import requests
import os

load_dotenv()

SLACK_ALERT_WEBHOOK = os.getenv("SLACK_ALERT_WEBHOOK")

def send_slack_notification(message):
    """
    
    sends a message to alerts slack channel

    """
    
    url = SLACK_ALERT_WEBHOOK
    data = {
        'text': message,
        # 'username': 'ig-reels-babe-page 🤖',
        # 'icon_emoji': ':warning:'
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        raise ValueError(f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")