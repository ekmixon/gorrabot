import datetime

from requests import Session

from api.gitlab import gitlab_session, GITLAB_API_PREFIX
from api.gitlab.utils import parse_api_date
from constants import GitlabLabels, decision_issue_message_interval


def get_issue(project_id: int, iid: int):
    url = '{}/projects/{}/issues/{}'.format(
            GITLAB_API_PREFIX, project_id, iid)
    res = gitlab_session.get(url)
    if res.status_code == 404:
        return
    res.raise_for_status()
    return res.json()


def get_issues(project_id: int, filters: dict = None):
    if filters is None:
        filters = {}
    url = f'{GITLAB_API_PREFIX}/projects/{project_id}/issues'
    res = gitlab_session.get(url, params=filters)
    res.raise_for_status()
    return res.json()


def get_decision_issues(project_id: int):
    filters = {
        'scope': 'all',
        'state': 'opened',
        'labels': 'waiting-decision',
        'per_page': 100,
    }
    issues = get_issues(project_id, filters)
    for issue in issues:
        if GitlabLabels.NO_ME_APURES in issue['labels']:
            continue
        updated_at = parse_api_date(issue['updated_at'])
        if datetime.datetime.utcnow() - updated_at > decision_issue_message_interval:
            yield issue


def get_accepted_issues(project_id: int):
    filters = {
        'scope': 'all',
        'labels': 'Accepted',
        'state': 'opened',
        'per_page': 100,
    }
    return get_issues(project_id, filters)


def update_issue(project_id: int, iid: int, data: dict):
    url = '{}/projects/{}/issues/{}'.format(
            GITLAB_API_PREFIX, project_id, iid)
    res = gitlab_session.put(url, json=data)
    res.raise_for_status()
    return res.json()
