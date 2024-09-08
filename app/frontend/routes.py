from flask import Blueprint, render_template
from ..extensions import mongo

frontend = Blueprint('frontend', __name__, url_prefix='')

@frontend.route('/', methods=["GET"])
def frontend():
    events = mongo.db.actions.find().sort({"created_At": -1})
    return render_template('index.html', events = events)