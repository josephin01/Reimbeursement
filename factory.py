from flask import Flask
from config import Config
from flask_cors import CORS
from api.user.views import user_api
from api.auth.views import auth_api
from api.expenseType.views import expenseType_api
from api.Purposes.views import purposeOfVisit_api
from api.manager.views import manager_api
from api.travelForm.views import travelForm_api
from config import db
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins="*")
    app.register_blueprint(user_api)
    app.register_blueprint(expenseType_api)
    app.register_blueprint(purposeOfVisit_api)
    app.register_blueprint(manager_api)
    app.register_blueprint(travelForm_api)
    app.register_blueprint(auth_api)
    db.init_app(app)
    JWTManager(app)
    with app.app_context():
        db.create_all()
        # db.drop_all()
    return app
