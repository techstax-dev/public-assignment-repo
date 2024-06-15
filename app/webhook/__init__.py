# from flask import Flask
# from app.webhook.routes import webhook_bp
# from app.webhook.extensions import mongo
# from config import config

# def create_app():
#     app = Flask(__name__)
#     app.config['MONGO_URI'] = config.MONGODB_URI
#     mongo.init_app(app)
    
#     app.register_blueprint(webhook_bp)
    
#     return app
