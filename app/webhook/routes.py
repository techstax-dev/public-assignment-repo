from flask import Blueprint, request, jsonify, render_template
from app.webhook.extensions import mongo
from config import config
from datetime import datetime
import os

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    if event_type == 'push':
        action = 'pushed'
        to_branch = data['ref'].split('/')[-1]
        author = data['pusher']['name']
    elif event_type == 'pull_request':
        action = 'submitted a pull request'
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        author = data['pull_request']['user']['login']
    elif event_type == 'pull_request' and data['action'] == 'closed' and data['pull_request']['merged']:
        action = 'merged branch'
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        author = data['pull_request']['user']['login']
    else:
        return jsonify({"message": "Event type not supported"}), 400
    
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
    event = {
        "author": author,
        "action": action,
        "from_branch": from_branch if 'from_branch' in locals() else '',
        "to_branch": to_branch,
        "timestamp": timestamp
    }
    mongo.cx[config.DB_NAME].webhook_events.insert_one(event)
    return jsonify({"message": "Webhook received"}), 200

@webhook_bp.route('/webhook/logs', methods=['GET'])
def get_webhook_logs():
    # Debug statement to check mongo object
    print("Mongo Object:", mongo)
    print("Mongo DB:", mongo.cx[config.DB_NAME])
    print("Database Name:", config.DB_NAME)
    
    logs = list(mongo.cx[config.DB_NAME].webhook_events.find({}, {'_id': 0}))
    return jsonify(logs), 200

@webhook_bp.route('/')
def home():
    print("Current directory:", os.getcwd())
    print("Template directory contents:", os.listdir('templates'))
    return render_template('index.html')
