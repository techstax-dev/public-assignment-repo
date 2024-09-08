from flask import Blueprint, json, request
from ..extensions import mongo
from ..github_event_management import get_event_doc

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():

    event_doc = get_event_doc()
    mongo.db.action.insert_one(event_doc)
    return {
        "event inserted": event_doc["action"]
    }, 200
