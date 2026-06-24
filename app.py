from flask import Flask , render_template,redirect,request,url_for,flash,Blueprint
from models import * 
from config import Config
from controllers.auth import auth_bp
from controllers.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth_bp,url_prefix="/auth")
app.register_blueprint(admin_bp,url_prefix="/admin")

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