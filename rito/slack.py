import requests
import json
import os

if 'RITO_SLACK_TOKEN' not in os.environ:
    print("To use Rito's slack functions, first create a Slack app on your workspace following these instructions: https://api.slack.com/messaging/sending#getting_started")
    print("After creating the app and requesting the right permissions, copy its auth token into an environment variable called RITO_SLACK_TOKEN")
    exit(1)

auth_token = os.environ['RITO_SLACK_TOKEN']

def send_slack_message(channel, text):
    payload = {
        "channel": channel,
        "text": text,
    }

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer {}".format(auth_token)
    }

    resp = requests.post("https://slack.com/api/chat.postMessage", data=json.dumps(payload), headers=headers)
    print(resp.text)