from wsgiref.util import request_uri
from flask import Flask, render_template, request, session, url_for, flash
from datetime import datetime
from pymongo import MongoClient
from werkzeug.utils import redirect
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongodb+srv://danhstnguyen:deankhoahocmaytinh@cluster0.jyc4s.mongodb.net/")
db = client["autostream_data"]
users_collection = db["users"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if "username" in session:
        flash("Bạn chưa đăng xuất !")
        return redirect(url_for("index"))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        email = request.form.get('email')
        dob = request.form.get('dob')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        occupation = request.form.get('occupation')
        family_size = request.form.get('family_size')
        maximum_budget = request.form.get('maximum_budget')

        # Bắt buộc điền đầy đủ các trường thông tin.
        if not all([username, password, email, dob, phone, gender, occupation, 
                    family_size, maximum_budget]):
            flash("Vui lòng điền đầy đủ thông tin !", "error")
            return render_template("register.html", username=username, name=name, email=email, dob=dob,
                                   phone=phone, gender=gender, occupation=occupation, family_size=family_size,
                                   maximum_budget=maximum_budget)

        # Kiểm tra định dạng email.
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("Email không đúng định dạng !", "error")
            return render_template("register.html", username=username, name=name, email=email, dob=dob,
                                   phone=phone, gender=gender, occupation=occupation, family_size=family_size,
                                   maximum_budget=maximum_budget, password = password)
        
        # Kiểm tra trùng khớp email trong cơ sở dữ liệu.
        if users_collection.find_one({"email": email}):
            flash("Email đã được liên kết với tài khoản khác !", "error")
            return render_template("register.html", username=username, name=name, email=email, dob=dob,
                                   phone=phone, gender=gender, occupation=occupation, family_size=family_size,
                                   maximum_budget=maximum_budget, password = password)
        
        # Tên đăng nhập trùng khớp với tên đã có.
        if users_collection.find_one({"username": username}):
            flash("Tên đăng nhập đã tồn tại !", "error")
            return render_template("register.html", username=username, name=name, email=email, dob=dob,
                                   phone=phone, gender=gender, occupation=occupation, family_size=family_size,
                                   maximum_budget=maximum_budget, password = password)

        # Yêu cầu mật khẩu mạnh.
        password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            flash("Mật khẩu cần có độ dài ít nhất 8 ký tự, bao gồm chữ viết hoa, chữ viết thường" + 
                  " chữ số, và ký tự đặc biệt.", "error")
            return render_template("register.html", username=username, name=name, email=email, dob=dob,
                                   phone=phone, gender=gender, occupation=occupation, family_size=family_size,
                                   maximum_budget=maximum_budget, password = password)

        user_data = {
            "username": username,
            "password": password,
            "name": name,
            "email": email,
            "dob": dob,
            "phone": phone,
            "gender": gender,
            "occupation": occupation,
            "family_size": family_size,
            "maximum_budget": maximum_budget
        }

        users_collection.insert_one(user_data)

        return redirect(url_for('verify_user'))

    return render_template("register.html")

@app.route('/verify_user')
def verify_user():
    return render_template("verify_user.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if "username" in session:
        flash("Bạn chưa đăng xuất !")
        return redirect(url_for("index"))
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = users_collection.find_one({"username": username, "password": password})

        if user:
            session["username"] = username
            session["name"] = user["name"]
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password. Try again!")
            return render_template("login.html", username = username, password = password)

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#-------------------------------------------------------------
# Vehicle searching site acts as vehicle_suggestion_algorithm.
#-------------------------------------------------------------
@app.route('/all_vehicles')
def all_vehicles():
    username = session.get("username")
    fengshui = fengshui_determination()
    occupation = get_user_occupation()
    gender = get_user_gender()
    family_size = get_user_family_size()
    budget = get_user_budget()
    return render_template('all_vehicles.html',
                           fengshui = fengshui, occupation = occupation, 
                           username = username, gender = gender, 
                           family_size = family_size, 
                           budget = budget)

def get_dob_from_database():
    username = session.get('username')
    if not username:
        return None

    user = users_collection.find_one({'username': username}, {'dob': 1})

    if user and 'dob' in user:
        try:
            dob = datetime.strptime(user['dob'], "%Y-%m-%d").date()
            return dob
        except ValueError:
            return None
    else:
        return None

def fengshui_determination():
    dob = get_dob_from_database()
    if not dob:
        return "Vui lòng đăng nhập để sử dụng chức năng."
    birth_year = dob.year
    can = birth_year % 10

     # Mapping Thiên Can
    if can in [0, 1]:  # Canh, Tân
        element_can = "Kim"
    elif can in [2, 3]:  # Nhâm, Quý
        element_can = "Thủy"
    elif can in [4, 5]:  # Giáp, Ất
        element_can = "Mộc"
    elif can in [6, 7]:  # Bính, Đinh
        element_can = "Hỏa"
    else:  # Mậu, Kỷ
        element_can = "Thổ"

    return f"Mệnh {element_can}"

def get_user_occupation():
    username = session.get('username')
    if not username:
        return None

    user = users_collection.find_one({"username": username}, {"occupation": 1})

    if user and "occupation" in user:
        try:
            return user["occupation"]
        except ValueError:
            return None
    else:
        return None
    
def get_user_gender():
    username = session.get('username')
    if not username:
        return None

    user = users_collection.find_one({"username": username}, {"gender": 1})

    if user and "gender" in user:
        try:
            return user["gender"]
        except ValueError:
            return None
    else:
        return None
    
def get_user_family_size():
    username = session.get('username')
    if not username:
        return None

    user = users_collection.find_one({"username": username}, {"family_size": 1})

    if user and "family_size" in user:
        try:
            return user["family_size"]
        except ValueError:
            return None
    else:
        return None
    
def get_user_budget():
    username = session.get('username')
    if not username:
        return None

    user = users_collection.find_one({"username": username}, {"maximum_budget": 1})

    if user and "maximum_budget" in user:
        try:
            return user["maximum_budget"]
        except ValueError:
            return None
    else:
        return None

#-------------------------------------------------------------
# Vehicle searching site acts as vehicle_suggestion_algorithm.
#-------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Listing details site then proceeds to Car_inpection_service and Down_payment_service.
#-------------------------------------------------------------------------------------
@app.route('/detail_of_listing')
def detail_of_listing():
    return render_template('detail-of-listing.html')

@app.route('/car-inspection', methods = ['GET', 'POST'])
def car_inspection_form():
    if request.method == 'POST':
        return redirect(url_for('confirmation'))

    vehicle_id = request.args.get('vehicle_id')
    listing_id = request.args.get('listing_id')

    return render_template('car_inspection_form.html',
                           vehicle_id = vehicle_id, listing_id = listing_id)

@app.route('/down_payment_form', methods = ['GET', 'POST'])
def down_payment():
    if request.method == "POST":
        return redirect(url_for("confirmation_3"))

    vehicle_id = request.args.get('vehicle_id')
    listing_id = request.args.get('listing_id')

    return render_template('down_payment.html', vehicle_id=vehicle_id, listing_id=listing_id)

@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    
    fee = request.args.get('fee')
    service = request.args.get('service')

    return render_template('checkout.html', fee = fee, service = service)

@app.route('/invoice')
def invoice():
    fee = request.args.get('fee')
    service = request.args.get('service')

    return render_template("invoice.html", fee = fee, service = service)

@app.route('/confirmation', methods = ['GET', 'POST'])
def confirmation():
    return render_template('confirmation.html')

@app.route('/confirmation2', methods = ['GET', 'POST'])
def confirmation_2():
    fee = request.args.get('fee')
    service = request.args.get('service')

    return render_template('confirmation_2.html', fee = fee, service = service)

@app.route('/confirmation_3', methods = ['GET', 'POST'])
def confirmation_3():
    fee = request.args.get('fee')
    service = request.args.get('service')

    return render_template("confirmation_3.html", fee = fee, service = service)

if __name__ == "__main__":
    app.run(debug = True)