from celery import Celery, shared_task
from flask_mail import Mail, Message
from flask import redirect, request, url_for
from website import create_app,db
from website.models import User, Address, Pitch, Time, Matchh, City, District, Bill
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from email import charset
charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')

def make_celery(app):
    #Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery

app = create_app()
sendit = Mail(app)
celery = make_celery(app)

@shared_task(name = 'celery.remind_email')
def remind_email(email, fullname, address, pitch, timeS, timeE):
    msg = Message("Nhắc bạn nhớ!", sender='noreply@demo.com',
        recipients=[email])
    msg.body = "Xin chào " + fullname + ", Còn khoảng 1 giờ nữa trận đấu của bạn sẽ diễn ra ở địa điểm: " + address + " - " + pitch + " vào lúc " + timeS + "-" + timeE +".\nXin cảm ơn!"
    sendit.send(msg)

@app.route('/bill', methods = ['GET', 'POST'])
def bill():
    if request.method == "POST":
        idMember = request.form.get("idMember")
        idMatch = request.form.get("idMatch")
        cost = request.form.get("cost")
        cost = cost + '.000'
        
        match = Matchh.query.get(idMatch)
        match.status = 'Đã thanh toán'
        match.statusPay = 'False'
        db.session.commit()

        new_bill = Bill(idMember, idMatch, cost)
        db.session.add(new_bill)
        db.session.commit()

        idAddress = match.idAddress
        address = Address.query.get(idAddress)
        host = User.query.get(address.idHost)
        member = User.query.get(idMember)
        idTime = match.idTime
        time = Time.query.get(idTime)
        idPitch = match.idPitch
        pitch = Pitch.query.get(idPitch)

        msg = Message("Thanh toán tiền cọc.", sender='noreply@demo.com',
            recipients=[host.email])
        msg.body =  "Xin chào " + host.fullname + ",\n" + member.fullname +" đã thanh toán tiền cọc đặt sân ở địa điểm: " + address.name + " - " + pitch.name + " vào khung giờ: " + time.timeS + " - " + time.timeE + ", thời gian diễn ra: " + match.date + " với số tiền cọc là " + cost +"đ. Bạn có thể kiểm tra trong phần Danh sách trận đấu.\nXin Cảm ơn!." 
        sendit.send(msg)

        dt_string = match.date + " " + time.timeS + ":00"
        dt_string = dt_string.replace('-', '/')

        dt_object1 = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")
        now = datetime.now()
        nowutc = datetime.utcnow()
        eta_datetime = nowutc + (dt_object1 - now)  - timedelta(hours=1)
        # print(member.email, member.fullname, address.name, pitch.name, time.timeS, time.timeE)
        celery.send_task('celery.remind_email', args=(member.email, member.fullname, address.name, pitch.name, time.timeS, time.timeE, ), eta= eta_datetime)

    return redirect(url_for('views.approve'))

if __name__ == "__main__":
    app.run(debug=True, port=888)