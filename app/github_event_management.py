from flask import request
import datetime

def get_event_details():

    git_event = request.headers.get('X-Github-Event')

    body = request.get_json()

    if git_event == "push":
        return git_event

    if body['action'] == "opened":
        return "pull"

    if body['pull_request']['merged_by'] is not None:
        return "merge"
    
    if git_event != "pull_request":
        raise "Invalid event."
    

def get_pull_doc():
    request_json = request.get_json()
    return {
        "request_id": str(request_json["pull_request"]["id"]),
        "author": request_json["pull_request"]["user"]["login"],
        "action": "PULL_REQUEST",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "created_At": request_json['pull_request']['created_at']
    }

def get_push_doc():
    request_json = request.get_json()
    return {
        "request_id": request_json['head_commit']['id'],
        "author": request_json['head_commit']['author']['username'],
        "action": "PUSH",
        "from_branch": request_json['ref'].split('/')[-1],
        "to_branch": request_json['ref'].split('/')[-1],
        "created_At": request_json['head_commit']['timestamp']
    }

def get_merge_doc():
    request_json = request.get_json()
    return {
        "request_id": str(request_json['pull_request']['id']),
        "author": request_json['pull_request']['merged_by']['login'],
        "action": "MERGE",
        "from_branch": request_json['pull_request']['head']['label'].split(':')[-1],
        "to_branch": request_json['pull_request']['base']['label'].split(':')[-1],
        "created_At": request_json['pull_request']['merged_at']
    }

def get_event_doc():

    event = get_event_details()

    if event == "push":
        event_doc = get_push_doc()
    
    elif event == "pull":
        event_doc = get_pull_doc()

    elif event == "merge":
        event_doc = get_merge_doc()

    event_doc["created_At"] = datetime.datetime.fromisoformat(action_object['created_At']).astimezone(datetime.timezone.utc)

    return event_doc