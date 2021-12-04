from flask import Flask,redirect
from db_connect import db
from flask_migrate import Migrate
import config
from flask_login import LoginManager

from models.models import User

login_manager=LoginManager()

    
def create_app():
    app = Flask(__name__)

    app.config.from_object(config) # config 에서 가져온 파일을 사용합니다.

    app.secret_key = "secret"
    app.config['SESSION_TYPE'] = 'filesystem'
 
    db.init_app(app) # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.signin"
    login_manager.login_message = u"로그인 후 이용해주시기 바랍니다."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(email=user_id).first()

    with app.app_context():
        db.create_all()

    from views import main_view, auth, book_views,rental,error_handler
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(rental.bp)
    app.register_blueprint(error_handler.bp)

    @app.route('/')
    def start():
        return redirect('/home/')

    return app

if __name__ == "__main__":
    app=create_app()
    app.run('0.0.0.0', 5000, debug=True)