from flask import Blueprint

def load(app):
    bp = Blueprint("dynamic_docker", __name__)

    # registrar rutas
    from .routes import register_routes
    register_routes(bp)

    app.register_blueprint(bp)

    # inicializar DB
    from .models import db
    db.create_all()

    # registrar challenge type (dummy)
    from .challenge import DynamicDockerChallenge