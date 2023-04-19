from flask import Flask
import os
import config

def create_app():
    templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

    # Load configuration
    app.config.from_object(config)

    from .routes.main import main_bp
    from .routes.callnotesgenerator import callnotesgenerator_bp
    from .routes.translator import translator_bp
    from .routes.summarizer import summarizer_bp
    from .routes.chatpdf import chatpdf_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(callnotesgenerator_bp)
    app.register_blueprint(translator_bp)
    app.register_blueprint(summarizer_bp)
    app.register_blueprint(chatpdf_bp)

    return app
