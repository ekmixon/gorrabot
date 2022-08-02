import os

from gorrabot.api.gitlab.projects import get_project_name
from gorrabot.api.slack import slack_session, SLACK_API_PREFIX
from gorrabot.config import config, DEBUG_MODE, NOTIFY_DEFAULT_CHANNEL, NOTIFY_DEBUG_CHANNEL


def check_can_send_slack_messages(project_id=None):
    """ Checks the send_message_to_slack config param is set """

    if not project_id:
        print("Invalid project id")
        return

    project_name = get_project_name(project_id)

    return (
        config()['projects'][project_name].get('send_message_to_slack', True)
        if project_name in config()['projects']
        else False
    )


def send_message_to_user(slack_user: str, text: str, slack_users_data: dict):
    slack_users_data = {
        elem["name"]: elem for elem in slack_users_data["members"] if not elem['deleted'] and not elem["is_bot"]
    }

    if slack_user not in slack_users_data:
        print(f"Ask for send message to user: {slack_user}, who is not in the slack api response")
        return None
    else:
        params = {
            "channel": slack_users_data[slack_user]['id'],
            "text": text,
            "as_user": True
        }
        return slack_session.post(
            f"{SLACK_API_PREFIX}/chat.postMessage", params=params
        )


def send_message_to_channel(slack_channel: str, text: str, project_id=None, force_send=False):

    can_send_message = check_can_send_slack_messages(project_id)

    if (not force_send) and (not can_send_message):
        # project cannot send message to Slack
        return

    params = {
        "channel": slack_channel,
        "text": text,
        "link_names": True
    }
    return slack_session.post(
        f"{SLACK_API_PREFIX}/chat.postMessage", params=params
    )


def send_message_to_error_channel(text: str, project_id: int, force_send=False):
    if not DEBUG_MODE and NOTIFY_DEFAULT_CHANNEL:
        send_message_to_channel(NOTIFY_DEFAULT_CHANNEL, text, project_id, force_send=True)


def send_debug_message(text: str):
    if 'DEBUG' in os.environ and NOTIFY_DEBUG_CHANNEL:
        send_message_to_channel(NOTIFY_DEBUG_CHANNEL, text)  # erich ID
