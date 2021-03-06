from flask import Blueprint, jsonify, redirect, request, url_for, flash
from . import create_app,db
from .models import User, Address, Pitch, Time, Matchh, City, District, Bill
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from email import charset
charset.add_charset('utf-8', charset.SHORTEST, charset.BASE64, 'utf-8')

crud = Blueprint("crud", __name__)

app = create_app()
sendit = Mail(app)

# user

@crud.route('/updateUser', methods = ['GET', 'POST'])
def updateUser():
    if request.method == 'POST':
        update_user = User.query.get(request.form.get('id'))

        update_user.fullname = request.form['fullName']
        update_user.birthday = request.form['birthdayDate']
        update_user.role = request.form['role']

        db.session.commit()

    return redirect(url_for('views.management_user'))

@crud.route('/deleteUser/<id>/', methods = ['GET', 'POST'])
def deleteUser(id):
    delete_user = User.query.get(id)
    delete_address = Address.query.filter_by(idHost = id)
    db.session.delete(delete_user)
    db.session.commit()
    for i in delete_address:
        db.session.delete(i)
        db.session.commit()
    delete_pitch = Pitch.query.filter_by(idHost = id)
    for i in delete_pitch:
        db.session.delete(i)
        db.session.commit()
    id_pitch = Pitch.query.filter_by(idHost = id)
    for i in id_pitch:
        id_time = Time.query.filter_by(idPitch = i.id)
        for j in id_time:
            db.session.delete(j)
            db.session.commit()
    delete_match = Matchh.query.filter_by(idMember = id)
    for i in delete_match:
        db.session.delete(i)
        db.session.commit()
    delete_bill = Bill.query.filter_by(idMember = id)
    for i in delete_bill:
        db.session.delete(i)
        db.session.commit()

    return redirect(url_for('views.management_user'))

@crud.route('/updateProfile', methods = ['GET', 'POST'])
def updateProfile():
    if request.method == 'POST':
        mess = ''

        update_profile = User.query.get(request.form.get('id'))

        if update_profile.email == request.form['email'] and update_profile.fullname == request.form['fullname'] and update_profile.gender == request.form['gender'] and update_profile.birthday == request.form['birthday'] and update_profile.phonenumber == request.form['phone'] and update_profile.linkFB == request.form['linkFB']:
            flash('B???n ch??a thay ?????i b???t k??? th??ng tin g??.', category='error')
        elif len(request.form['fullname']) < 3:
            flash('H??? t??n ph???i c?? ??t nh???t 3 k?? t???.', category='error')
        elif len(request.form['birthday']) < 1:
            flash('Ng??y sinh kh??ng ???????c ????? tr???ng.', category='error')
        elif len(request.form['phone']) < 1:
            flash('S??? ??i???n tho???i kh??ng ???????c ????? tr???ng.', category='error')
        elif len(request.form['email']) < 1:
            flash('Email kh??ng ???????c ????? tr???ng.', category='error')
        else:

            old_email = update_profile.email

            update_profile.fullname = request.form['fullname']
            update_profile.gender = request.form['gender']
            update_profile.birthday = request.form['birthday']
            update_profile.phonenumber = request.form['phone']
            update_profile.email = request.form['email']
            update_profile.linkFB = request.form['linkFB']

            email = update_profile.email
            
            email_exists = User.query.filter_by(email=email).first()

            if email_exists and update_profile.email != old_email:
                flash('Email ???? ???????c ????ng k??.', category='error')
            else:
                db.session.commit()
                flash('C???p nh???t th??nh c??ng!', category='success')

            return redirect(url_for('views.profile'))

    return redirect(url_for('views.profile'))

# address


@crud.route('/addAddress', methods = ['GET', 'POST'])
def addAddress():
    if request.method == 'POST':
        mess = ''

        idHost = request.form.get("idHost")
        name = request.form.get("name")
        address = request.form.get("address")
        city = request.form.get("city")
        district = request.form.get("district")
        linkAddress = request.form.get("linkAddress")
        iframe = request.form.get("iframeAddress")
        phone1 = request.form.get("phone1")
        phone2 = request.form.get("phone2")
        service = request.form.get("service")
        note = request.form.get("note")

        address_exists = Address.query.filter_by(address=address).first()

        if address_exists:
            mess = '?????a ch??? ???? ???????c t???o.'
        elif len(name) < 1:
            mess = 'B???n ph???i nh???p t??n ?????a ??i???m.'
        elif len(address) < 1:
            mess = 'B???n ph???i nh???p ?????a ch???.'
        elif city == '0':
            mess = 'B???n ch??a ch???n T???nh/Th??nh Ph???.'
        elif district == '0':
            mess = 'B???n ch??a ch???n Qu???n/Huy???n.'
        elif len(linkAddress) < 1:
            mess = 'B???n ch??a nh???p link li??n k???t google map.'
        elif len(iframe) < 1:
            mess = 'B???n ch??a nh???p iframe google map.'
        elif len(phone1) < 1:
            mess = 'B???n ph???i nh???p s??t li??n l???c 1.'
        
        if (mess != ''):
            return jsonify(status = 'not ok', mess = mess)
        else:
            city_name = City.query.get(city)
            district_name = District.query.get(district)

            new_address = Address( idHost, name, address, city_name.name, district_name.name, linkAddress, iframe, phone1, phone2, service, note)
            db.session.add(new_address)
            db.session.commit()
            flash('Th??m ?????a ??i???m th??nh c??ng.', category='success')
            
            return jsonify(status = 'ok', mess = mess)

    return redirect(url_for('views.management_address'))

@crud.route('/deleteAddress/<id>/', methods = ['GET', 'POST'])
def deleteAddress(id):
    delete_address = Address.query.get(id)
    delete_pitch = Pitch.query.filter_by(idAddress = id)
    db.session.delete(delete_address)
    db.session.commit()
    for i in delete_pitch:
        db.session.delete(i)
        db.session.commit()
    id_pitch = Pitch.query.filter_by(idAddress = id)
    for i in id_pitch:
        id_time = Time.query.filter_by(idPitch = i.id)
        for j in id_time:
            db.session.delete(j)
            db.session.commit()

    return redirect(url_for('views.management_address'))

@crud.route('/updateAddress', methods = ['GET', 'POST'])
def updateAddress():
    if request.method == 'POST':
        update_address = Address.query.get(request.form.get('id'))
        mess = ''

        old_address = update_address.address

        name = request.form.get("name")
        address = request.form.get("address")
        linkAddress = request.form.get("linkAddress")
        iframe = request.form.get("iframeAddress")
        phone1 = request.form.get("phone1")
        
        address_exists = Address.query.filter_by(address=address).first()

        if address_exists and address != old_address:
            mess = '?????a ch??? ???? ???????c t???o.'
        if len(name) < 1:
            mess = 'B???n ph???i nh???p t??n ?????a ??i???m.'
        elif len(address) < 1:
            mess = 'B???n ph???i nh???p ?????a ch???.'
        elif len(linkAddress) < 1:
            mess = 'B???n ch??a nh???p link li??n k???t google map.'
        elif len(iframe) < 1:
            mess = 'B???n ch??a nh???p iframe google map.'
        elif len(phone1) < 1:
            mess = 'B???n ph???i nh???p s??t li??n l???c 1.'
        
        if (mess != ''):
            return jsonify(status = 'not ok1', id = update_address.id, mess = mess)
        else:
            update_address.idHost = request.form.get("idHost")
            update_address.name = request.form.get("name")
            update_address.address = request.form.get("address")
            update_address.linkAddress = request.form.get("linkAddress")
            update_address.iframe = request.form.get("iframeAddress")
            update_address.phone1 = request.form.get("phone1")
            update_address.phone2 = request.form.get("phone2")
            update_address.service = request.form.get("service")
            update_address.note = request.form.get("note")
            db.session.commit()
            return jsonify(status = 'ok1', id = update_address.id, mess = mess)

    return redirect(url_for('views.management_address'))

# pitch
@crud.route('/addPitch', methods = ['GET', 'POST'])
def addPitch():
    if request.method == 'POST':
        mess = ''

        idAddress = request.form.get("idAddress")
        idHost = request.form.get("idHost")
        name = request.form.get("name")
        kind = request.form.get("kind")

        name_pitch_exists = Pitch.query.filter_by(name=name, idAddress =idAddress).first()

        if name_pitch_exists:
            mess = 'T??n s??n cho ?????a ??i???m n??y ???? t???n t???i'
        elif len(name) < 1:
            mess = 'B???n ch??a ?????t t??n s??n.'
        
        if mess != '':
            return jsonify(status = 'not ok', mess = mess)
        else:
            new_pitch = Pitch(idAddress, idHost, name, kind)
            db.session.add(new_pitch)
            db.session.commit()
            flash('Th??m s??n th??nh c??ng.', category='success')
            return jsonify(status = 'ok', mess = mess)

    return redirect(url_for('views.address_detail', id = idAddress))


@crud.route('/updatePitch', methods = ['GET', 'POST'])
def updatePitch():
    if request.method == 'POST':
        update_pitch = Pitch.query.get(request.form.get('id'))
        mess = ''

        old_name = update_pitch.name

        idAddress = request.form.get("idAddress")
        name = request.form.get("name")

        name_exists = Pitch.query.filter_by(name = name, idAddress = idAddress).first()

        if name_exists:
            mess = 'T??n s??n cho ?????a ??i???m n??y ???? t???n t???i'
        if len(name) < 1:
            mess = 'B???n ch??a ?????t t??n s??n.'

        if mess != '' and old_name != name:
            return jsonify(status = 'not ok1',id = update_pitch.id, mess = mess)
        else:
            update_pitch.idAddress = request.form.get("idAddress")
            update_pitch.idHost = request.form.get("idHost")
            update_pitch.name = request.form.get("name")
            update_pitch.kind = request.form.get("kind")
            db.session.commit()
            return jsonify(status = 'ok1', id = update_pitch.id, mess = mess)

    return redirect(url_for('views.address_detail'))

@crud.route('/deletePitch/<id>/', methods = ['GET', 'POST'])
def deletePitch(id):
    delete_pitch = Pitch.query.get(id)
    delete_time = Time.query.filter_by(idPitch = id)
    db.session.delete(delete_pitch)
    db.session.commit()
    for i in delete_time:
        db.session.delete(i)
        db.session.commit()


    return redirect(url_for('views.address_detail', id = delete_pitch.idAddress))


# time
@crud.route('/addTime', methods = ['GET', 'POST'])
def addTime():

    timeFormat = "%H:%M"

    if request.method == 'POST':
        mess = ''
        timeS = request.form.get("timeS")
        timeE = request.form.get("timeE")
        cost = request.form.get("cost")

        try:
            validtimeS = datetime.strptime(timeS, timeFormat)
            validtimeE = datetime.strptime(timeE, timeFormat)
        except ValueError:
            mess = 'Gi??? ch??a h???p l???.'
        
        if datetime.strptime(timeS,"%H:%M") >= datetime.strptime(timeE,"%H:%M"):
            mess = 'Gi??? b???t ?????u ph???i nh??? l??n gi??? k???t th??c.'

        if len(timeS) < 1:
            mess = 'B???n ch??a nh???p gi??? b???t ?????u.'
        elif len(timeE) < 1:
            mess = 'B???n ch??a nh???p gi??? k???t th??c.'
        elif len(cost) < 1:
            mess = 'B???n ch??a nh???p gi?? s??n.'
        
        if mess != '':
            return jsonify(status = 'not ok', mess = mess)
        else:
            new_time = Time(request.form.get("idPitch"), timeS, timeE, cost)
            db.session.add(new_time)
            db.session.commit()
            flash('Th??m khung gi??? th??nh c??ng.', category='success')
            return jsonify(status = 'ok', mess = mess)

    return redirect(url_for('views.pitch_detail', idAddress = request.form.get("idAddress"), idPitch = request.form.get("idPitch")))

@crud.route('/updateTime', methods = ['GET', 'POST'])
def updateTime():

    timeFormat = "%H:%M"

    if request.method == 'POST':
        update_time = Time.query.get(request.form.get('id'))
        mess = ''

        timeS = request.form.get("timeS")
        timeE = request.form.get("timeE")
        cost = request.form.get("cost")

        try:
            validtimeS = datetime.strptime(timeS, timeFormat)
            validtimeE = datetime.strptime(timeE, timeFormat)
        except ValueError:
            mess = 'Gi??? ch??a h???p l???.'
        
        if datetime.strptime(timeS,"%H:%M") >= datetime.strptime(timeE,"%H:%M"):
            mess = 'Gi??? b???t ?????u ph???i nh??? l??n gi??? k???t th??c.'

        if len(timeS) < 1:
            mess = 'B???n ch??a nh???p th???i gian b???t ?????u.'
        elif len(timeE) < 1:
            mess = 'B???n ch??a nh???p th???i gian k???t th??c.'
        elif len(cost) < 1:
            mess = 'B???n ch??a nh???p gi?? s??n.'
        
        if (mess != ''):
            return jsonify(status = 'not ok1', id = update_time.id, mess = mess)
        else:
            update_time.timeS = timeS
            update_time.timeE = timeE
            update_time.cost = cost
            db.session.commit()
            return jsonify(status = 'ok1', id = update_time.id, mess = mess)

    return redirect(url_for('views.pitch_detail'))

@crud.route('/deleteTime/<id>/', methods = ['GET', 'POST'])
def deleteTime(id):
    delete_time = Time.query.get(id)
    choice_pitch = Pitch.query.get(delete_time.idPitch)
    db.session.delete(delete_time)
    db.session.commit()

    return redirect(url_for('views.pitch_detail', idAddress = choice_pitch.idAddress, idPitch = delete_time.idPitch))

# Match
@crud.route('/addMatch', methods = ['GET', 'POST'])
def addMatch():
    if request.method == 'POST':

        idTime = request.form.get("idTime")
        idMember = request.form.get("idMember")
        idPitch = request.form.get("idPitch")
        idAddress = request.form.get("idAddress")
        dateTakePlace = request.form.get("dateTakePlace")
        phoneBackUp = request.form.get("phonebackup")
        note = request.form.get("note")

        pitch = Pitch.query.get(idPitch)
        idHost = pitch.idHost
        host = User.query.get(idHost)
        address_ = Address.query.get(idAddress)
        member = User.query.get(idMember)
        time = Time.query.get(idTime)

        new_match = Matchh( idTime, idMember, idPitch, idAddress, dateTakePlace, phoneBackUp, note, 'Ch??? duy???t', '', 'False')
        db.session.add(new_match)
        db.session.commit()

        msg = Message("Duy???t y??u c???u ?????t s??n.", sender='noreply@demo.com',
            recipients=[host.email])
        msg.body =  "Xin ch??o " + host.fullname + ",\n" +  member.fullname + " mu???n ?????t s??n ??? ?????a ??i???m: " + address_.name + " - " + pitch.name + " v??o khung gi???: " + time.timeS + " - " + time.timeE + ". H??y v??o website datsanbongonline12 ????? c?? th??? duy???t y??u c???u n??y.\nXin c???m ??n!" 
        sendit.send(msg)
    return redirect(url_for('views.approve'))

@crud.route('/updateStatus-yes/<id>/', methods = ['GET', 'POST'])
def updateStatus_yes(id):

    now = datetime.now() + timedelta(hours=6)
    dt_string = now.strftime("%d-%m-%Y %H:%M")

    setStatus = Matchh.query.get(id)
    setStatus.status = 'Ch???p nh???n'
    setStatus.datetimePay = dt_string
    setStatus.statusPay = 'True'
    db.session.commit()

    idMember = setStatus.idMember
    member = User.query.get(idMember)
    idAddress = setStatus.idAddress
    address = Address.query.get(idAddress)
    idPitch = setStatus.idPitch
    pitch = Pitch.query.get(idPitch)
    idTime = setStatus.idTime
    time = Time.query.get(idTime)

    msg = Message("K???t qu??? y??u c???u ?????t s??n.", sender='noreply@demo.com',
            recipients=[member.email])
    msg.body =  "Xin ch??o " + member.fullname + ",\n" + "Y??u c???u ?????t s??n ??? ?????a ??i???m: " + address.name + " - " + pitch.name + " v??o khung gi???: " + time.timeS + " - " + time.timeE + " ???? ???????c ch??? s??n Ch???p nh???n.Th???i h???n thanh to??n c???a y??u c???u ?????t s??n n??y l??: " + dt_string + ". N???u kh??ng thanh to??n tr?????c th???i h???n th?? y??u c???u ?????t s??n c???a b???n s??? b??? h???y. B???n c?? th??? ki???m tra trong ph???n Danh s??ch tr???n ?????u.\nXin C???m ??n!." 
    sendit.send(msg)

    return redirect(url_for('views.approve'))

@crud.route('/updateStatus-no/<id>/', methods = ['GET', 'POST'])
def updateStatus_no(id):
    setStatus = Matchh.query.get(id)
    setStatus.status = 'T??? ch???i'
    db.session.commit()

    idMember = setStatus.idMember
    member = User.query.get(idMember)
    idAddress = setStatus.idAddress
    address = Address.query.get(idAddress)
    idPitch = setStatus.idPitch
    pitch = Pitch.query.get(idPitch)
    idTime = setStatus.idTime
    time = Time.query.get(idTime)

    msg = Message("K???t qu??? y??u c???u ?????t s??n.", sender='noreply@demo.com',
            recipients=[member.email])
    msg.body =  "Xin ch??o " + member.fullname + ",\n" + "Y??u c???u ?????t s??n ??? ?????a ??i???m: " + address.name + " - " + pitch.name + " v??o khung gi???: " + time.timeS + " - " + time.timeE + " ???? ???????c ch??? s??n T??? ch???i v?? l?? do n??o ????. B???n c?? th??? ki???m tra trong ph???n Danh s??ch tr???n ?????u.\nXin C???m ??n!." 
    sendit.send(msg)

    return redirect(url_for('views.approve'))
