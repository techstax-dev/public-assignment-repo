from flask import Flask
from app.webhook.routes import webhook_bp
from app.webhook.extensions import mongo
from config import config
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'))
    app.config['MONGO_URI'] = config.MONGODB_URI
    mongo.init_app(app)
    
    # Debug statement to confirm MongoDB URI is set
    print("MongoDB URI:", app.config['MONGO_URI'])
    
    app.register_blueprint(webhook_bp)
    
    return app
