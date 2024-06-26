from flask import Blueprint, request, jsonify, render_template
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('webhook', __name__)
ui = Blueprint('ui', __name__)

@webhook.route('/', methods=['POST'])
def handle_webhook():
    data = request.json

    print(f"github payload is {data} \n\n")

    event_type = request.headers.get('X-GitHub-Event')
    if event_type == 'push':
        handle_push(data)
    elif event_type == 'pull_request':
        handle_pull_request(data)

    return jsonify({"status": "success"}), 200

def handle_push(data):

    print(f"inside push function \n\n")
    author = data['pusher']['name']
    to_branch = data['ref'].split('/')[-1]
    timestamp = datetime.utcnow()
    
    record = {
        "event": "push",
        "author": author,
        "to_branch": to_branch,
        "timestamp": timestamp
    }
    mongo.db.events.insert_one(record)

def handle_pull_request(data):

    print(f"inside pull req function \n\n")

    action = data['action']
    author = data['pull_request']['user']['login']
    from_branch = data['pull_request']['head']['ref']
    to_branch = data['pull_request']['base']['ref']
    timestamp = datetime.utcnow()
    
    if action == 'closed' and data['pull_request']['merged']:
        
        print(f"inside merge function \n\n")
        record = {
            "event": "merge",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }
    else:
                
        print(f"inside pull requst function \n\n")
        record = {
            "event": "pull_request",
            "author": author,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

    mongo.db.events.insert_one(record)

@webhook.route('/events', methods=['GET'])
def get_events():
    events = list(mongo.db.events.find().sort("timestamp", -1).limit(10))
    for event in events:
        event["_id"] = str(event["_id"])
    return jsonify(events)

@ui.route('/')
def index():
    return render_template('index.html')
