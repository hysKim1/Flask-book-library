from flask import Flask,redirect
from db_connect import db
from flask_migrate import Migrate
import config
import os

def create_app():
    app = Flask(__name__)

    app.config.from_object(config) # config 에서 가져온 파일을 사용합니다.

    db.init_app(app) # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)
    with app.app_context():
        db.create_all()

    from views import main_view
    from views import auth, book_views,rental
    app.register_blueprint(main_view.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(book_views.bp)
    app.register_blueprint(rental.bp)

    app.secret_key = "secret"
    app.config['SESSION_TYPE'] = 'filesystem'
    
    @app.route('/')
    def welcome():
        return redirect('/home/')

    return app

if __name__ == "__main__":
    app=create_app()
    app.run('0.0.0.0', 5000, debug=True)