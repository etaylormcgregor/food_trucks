from flask_sqlalchemy import SQLAlchemy
from flask import Flask

 
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'af3ceaa070fb4e3df09704de5d5ef0511a6455e978d93f33'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'permits.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

        from utils import get_permits
        from models.permit import Permit

        db.session.query(Permit).delete()
        
        permits = get_permits()
        db.session.add_all(permits)
        db.session.commit()
    
    return app
