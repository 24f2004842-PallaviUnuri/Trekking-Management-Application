from flask import Flask , render_template,redirect,request,url_for,flash,Blueprint
from models import * 
from config import Config
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.staff import staff_bp
from controllers.trekker import trekker_bp
from flask_login import LoginManager 



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "warning"





app.register_blueprint(auth_bp,url_prefix="/auth")
app.register_blueprint(admin_bp,url_prefix="/admin")
app.register_blueprint(staff_bp,url_prefix="/staff")
app.register_blueprint(trekker_bp,url_prefix="/trekker")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#create admin superuser 
def create_admin():
    """Create an admin superuser if one doesn't exist."""
    admin = User.query.filter_by(role="Admin").first()
    if not admin:
        superuser = User(
            name  = "admin",
            email = "admin@admin.com",
            role  = "Admin",
            password = "pass"
        )
        
        db.session.add(superuser)
        db.session.commit()
        print("Admin created")
    else:
        print("Admin already exits.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)