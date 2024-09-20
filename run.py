from flask import Flask, jsonify
from db.connection import db
from app.routes.user_routes import user_bp
from flask_migrate import Migrate
from marshmallow import ValidationError

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(user_bp, url_prefix='/api')

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({"errors": err.messages}), 400

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
