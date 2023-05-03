from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

#gives us access to database operations
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    
    #set up database
    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    
    #connect db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)
    
    #import routes
    from .routes import crystal_bp
    #register the blueprint
    app.register_blueprint(crystal_bp)
    
    from app.models.crystal import Crystal
    
    return app