from flask import Flask
from flask_restx import Api


def create_app():
    from wh.api_namespace import api_namespace
    from wh.admin_namespace import admin_namespace

    application = Flask(__name__)
    api = Api(application, version='0.1', title='Warhouse Backend API',
              description='A Simple CRUD API')

    from wh.db import db, db_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config.update(db_config)
    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)

    return application
