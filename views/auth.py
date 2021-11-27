from flask  import Blueprint, request, session, redirect, url_for, render_template, flash,g
from db_connect import db
from models.models import User
from werkzeug.security import check_password_hash,generate_password_hash
import re

bp = Blueprint('auth', '__name__', url_prefix='/user')

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email', None)
        pwd = request.form.get('pwd', None)

        message, messageType = None, None

        user = User.query.filter(User.email == email).first()

        if not user:
            message, messageType = '등록된 이메일이 아닙니다. 다시 확인해주세요.','danger'
        elif not check_password_hash(user.password,pwd):
            message, messageType = '비밀번호가 틀렸습니다. 다시 확인해주세요.','danger'
        else:
            if not message:
                session.clear()
                session['user_id'] = email
                session['name'] =user.username
                flash('로그인 성공!')
                return redirect('/')
        flash(message=message, category=messageType)
        
    return render_template('login.html')

@bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('main.home'))

@bp.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email = request.form.get('email', None)
        username = request.form.get('username', None)
        pwd = request.form.get('pwd', None)
        pwd2 = request.form.get('val_pwd', None)

        message, messageType = None, None
        #영문,숫자,특수문자
        val_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        #한글,영어, 띄어쓰기 (외국인인 경우 띄어쓰기 필요 ㅠ)
        val_username = re.compile('^[가-힣a-zA-Z\s]+$')
        #최소 8자의  비빌번호 최소 하나의 특수문자, 영소문자, 숫자  포함
        #개인정보 보호초지 기준 : 3가지중 최소 2개
        val_pwd1 = re.compile('^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[~!@#$%^&*+=-]).{8,100}$')
        val_pwd2 = re.compile('^[a-zA-Z0-9]{10,100}$')
        val_pwd3 = re.compile('^[a-zA-Z~!@#$%^&*]{10,100}$')
        val_pwd4 = re.compile('^[\d~!@#$%^&*]{10,100}$')

        if  val_username.match(username) is None:
            message, messageType = '이름이 유효하지 않습니다.', 'danger'
        elif  val_email.match(email) is None:
            message, messageType = '아이디가 유효하지 않습니다.', 'danger'
        elif (val_pwd1.match(pwd) or val_pwd2.match(pwd) or val_pwd3.match(pwd) or val_pwd4.match(pwd)) is None:
            message, messageType = '비밀번호는 영문/숫자/특수문자(~!@#$%^&*) 3개 조합으로 최소 8자리 이상 입력하거나 개 조합으로 최소 10자리 이상 입력해주세요.', 'danger'
        elif pwd != pwd2:
            message, messageType = '비밀번호를 다시 확인해주십시오.', 'danger'
        else:
            user = User.query.filter(User.email == email).first()
            if user:
                message, messageType = '해당 계정은 이미 등록되었습니다.', 'warning'

        if not message:
            user = User(username, email, generate_password_hash(pwd))

            db.session.add(user)
            db.session.commit()
            flash('회원 가입이 완료되었습니다.')
            return redirect(url_for('main.home')) 

        flash(message=message, category=messageType)

    return render_template('signup.html')


