from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/srv_monitor'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # IMPORTS AQUÍ
    from app.routes.dashboard import dashboard_bp
    from app.routes.equipos import equipos_bp
    from app.routes.api.checkin import api_bp

    # BLUEPRINTS
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(api_bp)

    return app