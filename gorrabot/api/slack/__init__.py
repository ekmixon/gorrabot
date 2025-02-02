import os
import requests

BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_API_PREFIX = "https://slack.com/api"

slack_session = requests.Session()
slack_session.params["token"] = BOT_TOKEN
