from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = "auth.login"            # Ruta de login
login_manager.login_message_category = "warning"   # Categoría de mensaje Flash

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Registrar Blueprints
    from app.auth.auth import auth_bp
    from app.main.routes import main_bp  # si tenés esto creado

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app