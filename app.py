# app.py
from flask import Flask
from controllers import (
    event_controller,
    participant_controller,
    speaker_controller,
    vendor_controller,
    feedback_controller,
    budget_controller,
)

def create_app():
    app = Flask(__name__)
    # Registro dos blueprints dos controllers
    app.register_blueprint(event_controller.bp)
    app.register_blueprint(participant_controller.bp)
    app.register_blueprint(speaker_controller.bp)
    app.register_blueprint(vendor_controller.bp)
    app.register_blueprint(feedback_controller.bp)
    app.register_blueprint(budget_controller.bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
