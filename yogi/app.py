import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import config


login_manager = LoginManager()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.skills import skills_bp
    from routes.exchange import exchange_bp
    from routes.chat import chat_bp
    from routes.admin import admin_bp
    from routes.certificates import certificates_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(skills_bp, url_prefix='/skills')
    app.register_blueprint(exchange_bp, url_prefix='/exchange')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(certificates_bp, url_prefix='/certificates')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(email='admin@skillswap.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@skillswap.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin@skillswap.com / admin123")
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, port=5000)

