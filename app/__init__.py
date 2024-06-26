from flask import Flask
from app.extensions import init_mongo
from app.webhook.routes import webhook, ui

def create_app():
    app = Flask(__name__)

    init_mongo(app)

    app.register_blueprint(webhook, url_prefix='/webhook')
    app.register_blueprint(ui, url_prefix='/ui')
    
    return app
