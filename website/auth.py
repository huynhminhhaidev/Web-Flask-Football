from flask import Blueprint, flash, redirect, render_template, request, url_for
from . import create_app, db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import random
import string

auth = Blueprint("auth", __name__)

app = create_app()
sendit = Mail(app)

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        mess = ''
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if len(email) <= 0:
            mess = 'Bạn chưa nhập email.'
        elif len(password) <= 0:
            mess = 'Bạn chưa nhập mật khẩu.'
        elif not user:
            mess = 'Email không tồn tại.'
        
        if mess != '':
            return render_template('login.html', mess = mess, email = email)
        else:
            if check_password_hash(user.password, password):
                flash('Đăng nhập thành công!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                mess = 'Mật khẩu không chính xác.'
                return render_template('login.html', mess = mess, email = email)
    
    return render_template("login.html")

@auth.route("/sign-up",  methods=["POST", "GET"])
def sign_up():

    if request.method == 'POST':
        mess = ''
        fullname = request.form.get("fullname")
        gender = request.form.get("gender")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        email = request.form.get("email")
        role = request.form.get("role")
    
        email_exists_user = User.query.filter_by(email=email).first()

        if email_exists_user:
            mess = 'Email đã được đăng ký.'
        elif len(fullname) < 3:
            mess = 'Họ tên phải có ít nhất 3 ký tự.'            
        elif len(phone) <= 0:
            mess = 'Bạn chưa nhập số điện thoại.'            
        elif len(email) <= 0:
            mess = 'Bạn chưa nhập email.'            
        elif len(birthday) <= 0:
            mess = 'Bạn chưa nhập ngày sinh.'
            
        if mess != '':
            return render_template('signup.html', mess = mess, fullname =fullname, birthday = birthday, phone = phone, email = email)    
        else:
            password = id_generator()

            new_user = User(fullname, gender, birthday, phone, email, role, generate_password_hash(password, method='sha256'), '')
            db.session.add(new_user)
            db.session.commit()

            msg = Message("Đăng ký thành công.", sender='noreply@demo.com',
            recipients=[email])
            msg.body =  "Xin chào " + fullname + ",\n" + "Mật khẩu của bạn để đăng nhập vào website là: " + password + "." +"\nXin Cảm ơn!." 
            sendit.send(msg)

            flash('Đăng ký thành công. Hãy vào gmail để lấy mật khẩu.', category='success')

            return redirect(url_for('auth.login'))

    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/forget-password", methods = ['GET', 'POST'])
def forget_password():

    if request.method == 'POST':

        mess = ''

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if len(email) < 1:
            mess = 'Bạn phải nhập email.'
        elif not user:
            mess = 'Email không tồn tại.'

        if mess != '':
            return render_template("forget-password.html", mess = mess, email = email)
        else:
            update_password = User.query.filter_by(id = user.id).first()
            update_password.password = generate_password_hash('123456789', method='sha256')
            db.session.commit()
            msg = Message("Cấp lại mật khẩu.", sender='noreply@demo.com',
                recipients=[email])
            msg.body = "Mat khau moi cua ban la: 123456789. Ban co the doi mat khau bang cach chon Tai Khoan => Doi mat khau. Xin cam on!"
            sendit.send(msg)
            flash('Mật khẩu mới đã được gửi vào email của bạn.', category='success')
            return redirect(url_for("auth.forget_password"))
    return render_template("forget-password.html")

@auth.route("/change-password", methods = ['GET', 'POST'])
@login_required
def change_password():

    if request.method == 'POST':
        mess = ''

        emailAddress = request.form.get("email")
        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("newPassword")

        user = User.query.filter_by(email=emailAddress).first()

        if len(oldPassword) < 1:
            mess = 'Bạn chưa nhập mật khẩu.'
        elif len(newPassword) < 1:
            mess = 'Bạn chưa nhập mật khẩu mới.'
        elif len(newPassword) < 6:
            mess = 'Mật khẩu mới phải có ít nhất 6 kí tự.'

        if mess != '':
            return render_template("change-password.html", user = current_user, mess = mess)
        else:
            if check_password_hash(user.password, oldPassword):
                user.password = generate_password_hash(newPassword, method='sha256')
                db.session.commit()
                flash('Đổi mật khẩu thành công!', category='success')
                return redirect(url_for('auth.change_password'))
            else:
                mess = 'Mật khẩu không chính xác.'
                return render_template("change-password.html", user = current_user, mess = mess)

    return render_template("change-password.html", user = current_user)