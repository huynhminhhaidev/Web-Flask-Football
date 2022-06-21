from unicodedata import name
from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from flask_login import current_user, login_required
import sqlalchemy
from .models import User, Address, Pitch, Time, Matchh, City, District, Bill
from . import db, create_app
from flask_mail import Mail, Message
from datetime import date, datetime, timedelta
import itertools

import re
def change_date_format(dt):
    return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

views = Blueprint("views", __name__)

app = create_app()
sendit = Mail(app)

@views.route("/home", methods = ['GET', 'POST'])
@views.route("/", methods = ['GET', 'POST'])
def home():

    if request.method == "POST":
        search = request.form.get("search")
        id_city = request.form.get("city")
        id_district = request.form.get("district")
        kind = request.form.get("kind")

        city = City.query.get(id_city)
        district = District.query.get(id_district)
        tag = "%{}%".format(search)
        name_upper = ('Sân bóng đá cả nước').upper()
        name_city = ''
        name_district = ''
        
        if id_city == '0' and id_district == '0' and kind == '0':
            results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag))\
                            .join(Pitch, Pitch.idAddress == Address.id)
            asc_expression = sqlalchemy.sql.expression.asc(Address.name)
            results = results1.order_by(asc_expression)

            all_address = []

            for i, j in results:
                all_address.append([i.id, i.name, j.kind])
            
            all_address.sort()
            all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        elif id_city == '0' and id_district == '0' and kind != '0':
            results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag))\
                            .join(Pitch, Pitch.idAddress == Address.id).filter_by(kind = kind)
            asc_expression = sqlalchemy.sql.expression.asc(Address.name)
            results = results1.order_by(asc_expression)

            all_address = []

            for i, j in results:
                all_address.append([i.id, i.name, j.kind])
            
            all_address.sort()
            all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        elif id_city != '0' and id_district == '0' and kind == '0':
            name_city = city.name
            results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag)).filter_by(city = name_city)\
                        .join(Pitch, Pitch.idAddress == Address.id)
            asc_expression = sqlalchemy.sql.expression.asc(Address.name)
            results = results1.order_by(asc_expression)

            all_address = []

            for i, j in results:
                all_address.append([i.id, i.name, j.kind])
            
            all_address.sort()
            all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        elif id_city != '0' and id_district == '0' and kind != '0':
            name_city = city.name
            results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag)).filter_by(city = name_city)\
                        .join(Pitch, Pitch.idAddress == Address.id).filter_by(kind = kind)
            asc_expression = sqlalchemy.sql.expression.asc(Address.name)
            results = results1.order_by(asc_expression)

            all_address = []

            for i, j in results:
                all_address.append([i.id, i.name, j.kind])
            
            all_address.sort()
            all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        else:
            name_city = city.name
            name_district = district.name
            results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag)).filter_by(city = name_city, district = name_district)\
                            .join(Pitch, Pitch.idAddress == Address.id)
            asc_expression = sqlalchemy.sql.expression.asc(Address.name)
            results = results1.order_by(asc_expression)

            all_address = []

            for i, j in results:
                all_address.append([i.id, i.name, j.kind])
            
            all_address.sort()
            all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        
        all_city = db.session.query(City).all()

        if (name_city != ''):
            name_upper = ('Sân bóng đá ' + name_city).upper()

        return render_template("home.html", user = current_user, cities = all_city, search = search, id_city = id_city, id_district = id_district, kind = kind, addresses = all_address, name_upper = name_upper)
    else:
        tag = "%{}%".format('')

        results1 = db.session.query(Address, Pitch).filter(Address.name.like(tag))\
                        .join(Pitch, Pitch.idAddress == Address.id)
        
        asc_expression = sqlalchemy.sql.expression.asc(Address.name)
        results = results1.order_by(asc_expression)

        all_address = []

        for i, j in results:
            all_address.append([i.id, i.name, j.kind])
        
        all_address.sort()
        all_address = list(all_address for all_address,_ in itertools.groupby(all_address))

        all_city = db.session.query(City).all()

        name_upper = ('Sân bóng đá cả nước').upper()

        return render_template("home.html", user = current_user, cities = all_city, search = '', addresses = all_address, name_upper = name_upper)

# for user
@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user = current_user)

# for admin
@views.route('/management-user')
@login_required
def management_user():

    query_users = db.session.query(User)
    asc_expression = sqlalchemy.sql.expression.asc(User.fullname)
    all_users = query_users.order_by(asc_expression)


    return render_template("management-user.html", user = current_user, users = all_users)

# for chu san
@views.route('/management-address')
@login_required
def management_address():

    all_address1 = db.session.query(Address).filter_by(idHost = current_user.id)
    asc_expression = sqlalchemy.sql.expression.asc(Address.name)
    all_address = all_address1.order_by(asc_expression)
        
    all_city = db.session.query(City).all()

    return render_template('management-address.html', user = current_user, addresses = all_address, cities = all_city, districts = '')

@views.route('/getDistrict', methods = ['GET', 'POST'])
@login_required
def getDistrict():

    if request.method == 'POST':
        text_districts = '<option value="0" selected>Quận/Huyện</option>'
        id = request.form.get("id")

        districts = db.session.query(District).filter_by(idCity = id)
        for i in districts:
            text_districts = text_districts + '<option value="' + i.id +'">' + i.name +'</option>'

    return jsonify(districts = text_districts)

@views.route('/address-detail/<id>', methods = ['GET', 'POST'])
@login_required
def address_detail(id):

    address_detail = Address.query.get(id)
    all_pitch1 = db.session.query(Pitch).filter_by(idAddress = id)
    asc_expression = sqlalchemy.sql.expression.asc(Pitch.name)
    all_pitch = all_pitch1.order_by(asc_expression)

    near_address = db.session.query(Address, Pitch).filter(Address.city == address_detail.city, Address.name != address_detail.name)\
                        .join(Pitch, Pitch.idAddress == Address.id)
    
    all_near_address = []

    for i, j in near_address:
        all_near_address.append([i.id, i.name, j.kind])
    
    all_near_address.sort()
    all_near_address = list(all_near_address for all_near_address,_ in itertools.groupby(all_near_address))

    return render_template('address-detail.html', user = current_user, address_detail = address_detail, pitches = all_pitch, all_near_address = all_near_address)

# for thanh vien and chu san

@views.route('/approve')
@login_required
def approve():

    now = datetime.now()
    current_time1 = now.strftime("%H:%M")
    current_day1 = now.strftime("%d-%m-%Y")

    all_wait_match = db.session.query(Matchh, Time).filter_by(status = 'Chờ duyệt')\
                            .join(Time, Time.id == Matchh.idTime)
    for match, time in all_wait_match:
        if match.status == 'Chờ duyệt':
            bool_time =  datetime.strptime(time.timeS,"%H:%M") > datetime.strptime(current_time1,"%H:%M")
            bool_date = datetime.strptime(match.date, "%d-%m-%Y") >= datetime.strptime(current_day1,"%d-%m-%Y")
            if bool_date == False and bool_time == False:
                setStatus = Matchh.query.get(match.id)
                setStatus.status = 'Quá hạn'
                db.session.commit()
            elif bool_date == False and bool_time == True:
                setStatus = Matchh.query.get(match.id)
                setStatus.status = 'Quá hạn'
                db.session.commit()

    if current_user.role == "ThanhVien":
        results1 = db.session.query(Matchh, Time, Pitch, User, Address).filter_by(idMember = current_user.id)\
                            .join(Time, Time.id == Matchh.idTime)\
                            .join(Pitch, Pitch.id == Matchh.idPitch)\
                            .join(User, User.id == Matchh.idMember)\
                            .join(Address, Address.id == Matchh.idAddress)
        asc_expression = sqlalchemy.sql.expression.desc(Matchh.date)
        results = results1.order_by(asc_expression)
    else:
        results1 = db.session.query(Matchh, Time, Pitch, User, Address)\
                            .join(Time, Time.id == Matchh.idTime)\
                            .join(Pitch, Pitch.id == Matchh.idPitch).filter_by(idHost = current_user.id)\
                            .join(User, User.id == Matchh.idMember)\
                            .join(Address, Address.id == Matchh.idAddress)
        asc_expression = sqlalchemy.sql.expression.desc(Matchh.date)
        results = results1.order_by(asc_expression)
    
    all_accept_match = db.session.query(Matchh).filter_by(status = 'Chấp nhận', statusPay = 'True')
    
    dt_string = now.strftime("%d-%m-%Y %H:%M")
    now_check = datetime.strptime(dt_string, "%d-%m-%Y %H:%M")

    for i in all_accept_match:
        if datetime.strptime(i.datetimePay, "%d-%m-%Y %H:%M") < now_check:
            match_change = Matchh.query.get(i.id)
            match_change.status = 'Không thanh toán'
            match_change.statusPay = 'False'
            db.session.commit()

    return render_template('approve.html', user = current_user, results = results)

@views.route('/pitch-detail/<idAddress>/<idPitch>', methods = ['GET', 'POST'])
@login_required
def pitch_detail(idAddress, idPitch):

    timeFormat = "%H:%M"

    today = date.today()
    
    address_detail = Address.query.get(idAddress)
    pitch_detail = Pitch.query.get(idPitch)
    all_time = Time.query.filter_by(idPitch = idPitch)

    all_match_accept = []
    
    if request.method == "POST":
        
        dates = []

        value_filter_time_S = request.form.get("filter_time_S")
        value_filter_time_E = request.form.get("filter_time_E")

        if value_filter_time_S == '':
            value_filter_time_S = "6:00"
        
        if value_filter_time_E == '':
            value_filter_time_E = "22:00"

        try:
            validtimeS = datetime.strptime(value_filter_time_S, timeFormat)
            validtimeE = datetime.strptime(value_filter_time_E, timeFormat)
        except ValueError:
            value_filter_time_S = "6:00"
            value_filter_time_E = "22:00"

        if datetime.strptime(value_filter_time_S,"%H:%M") >= datetime.strptime(value_filter_time_E,"%H:%M"):
            value_filter_time_S = "6:00"
            value_filter_time_E = "22:00"

        filter_date_from = datetime.strptime(change_date_format(request.form.get("filter_date_from")), "%d-%m-%Y")
        filter_date_to = datetime.strptime(change_date_format(request.form.get("filter_date_to")), "%d-%m-%Y")

        current_date = datetime.strptime(change_date_format(str(today)), "%d-%m-%Y")

        if filter_date_from <= current_date:
            filter_date_from = current_date + timedelta(days=1)
        
        if filter_date_to < filter_date_from:
            filter_date_to = filter_date_from + timedelta(days=3)

        value_filter_date_from = datetime.strftime(filter_date_from, "%Y-%m-%d")

        between_dates = (filter_date_to - filter_date_from).days

        dates.append(datetime.strftime(filter_date_from, "%d-%m-%Y"))
        
        for i in range(0, between_dates):
            filter_date_from += timedelta(days=1)
            dates.append(datetime.strftime(filter_date_from, "%d-%m-%Y"))

        value_filter_date_to = datetime.strftime(filter_date_from, "%Y-%m-%d")
    else:

        value_filter_time_S = "6:00"
        value_filter_time_E = "22:00"

        dates = []

        current_date = datetime.strptime(change_date_format(str(today)), "%d-%m-%Y")

        current_date = current_date + timedelta(days=1)

        future_date = current_date + timedelta(days=3)

        between_dates = (future_date - current_date).days

        dates.append(datetime.strftime(current_date, "%d-%m-%Y"))

        for i in range(0, between_dates):
            current_date += timedelta(days=1)
            dates.append(datetime.strftime(current_date, "%d-%m-%Y"))

        value_filter_date_from = datetime.strftime(datetime.strptime(change_date_format(str(today)), "%d-%m-%Y") + timedelta(days=1), "%Y-%m-%d")
        value_filter_date_to = datetime.strftime(datetime.strptime(change_date_format(str(today)), "%d-%m-%Y") + timedelta(days=4), "%Y-%m-%d")

    value_filter_date_min = datetime.strftime(datetime.strptime(change_date_format(str(today)), "%d-%m-%Y") + timedelta(days=1), "%Y-%m-%d")
    
    match_accept = db.session.query(Matchh).filter_by(status = 'Đã thanh toán', idPitch = idPitch)

    for i in dates:
        for j in all_time:
            if datetime.strptime(j.timeS,"%H:%M") >= datetime.strptime(value_filter_time_S,"%H:%M") and datetime.strptime(j.timeE,"%H:%M") <= datetime.strptime(value_filter_time_E,"%H:%M"):
                all_match_accept.append([i, j.id])
    
    for i in match_accept:
        if [i.date,i.idTime] in all_match_accept:
            all_match_accept.remove([i.date,i.idTime])

    near_address = db.session.query(Address, Pitch).filter(Address.city == address_detail.city, Address.name != address_detail.name)\
                        .join(Pitch, Pitch.idAddress == Address.id)
    
    all_near_address = []

    for i, j in near_address:
        all_near_address.append([i.id, i.name, j.kind])
    
    all_near_address.sort()
    all_near_address = list(all_near_address for all_near_address,_ in itertools.groupby(all_near_address))

    return render_template('pitch-detail.html', user = current_user, address_detail = address_detail, pitch_detail = pitch_detail, times = all_time, dates = dates, all_match_accept = all_match_accept, all_near_address = all_near_address, value_filter_date_from = value_filter_date_from, value_filter_date_to = value_filter_date_to, value_filter_date_min = value_filter_date_min, value_filter_time_S = value_filter_time_S, value_filter_time_E = value_filter_time_E)


@views.route('/list-bill', methods = ['GET', 'POST'])
@login_required
def list_bill():
    # all_bill = db.session.query(Bill).filter_by(idMember = current_user.id)

    all_bills = db.session.query(Matchh, Address, User, Time, Pitch, Bill)\
                            .join(User, User.id == Matchh.idMember)\
                                .join(Time, Time.id == Matchh.idTime)\
                                    .join(Pitch, Pitch.id == Matchh.idPitch)\
                                        .join(Bill, Bill.idMatch == Matchh.id).filter_by(idMember = current_user.id)\
                                            .join(Address, Address.id == Matchh.idAddress)

    return render_template('list-bill.html', user = current_user, all_bills = all_bills)