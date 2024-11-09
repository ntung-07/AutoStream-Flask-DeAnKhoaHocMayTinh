from wsgiref.util import request_uri

from flask import Flask, render_template, request, session, url_for, flash
from datetime import datetime
from pymongo import MongoClient
from werkzeug.utils import redirect

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

        if username and password and email and dob and phone and gender and occupation and family_size and maximum_budget:
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

            return redirect(url_for('login'))

        else:
            flash("Please fill in all fields!", "error")
            return render_template("register.html")
    return render_template("register.html")

# Sign in
@app.route('/login', methods = ['GET', 'POST'])
def login():
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
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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

@app.route('/confirmation', methods = ['GET', 'POST'])
def confirmation():
    return render_template('confirmation.html')

@app.route('/checkout', methods = ['GET', 'POST'])
def checkout():
    if request.method == "POST":
        return redirect(url_for('confirmation_2'))

    return render_template('checkout.html')

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

    # This is for testing only. Official program will require a formula.
    if birth_year == 2004:
        return 'Mệnh Thủy'
    elif birth_year == 1978:
        return 'Mệnh Hỏa'
    elif birth_year == 1920:
        return "Mệnh Mộc"
    else:
        return "Under development.."

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

@app.route('/all_vehicles')
def all_vehicles():
    username = session.get("username")
    fengshui = fengshui_determination()
    occupation = get_user_occupation()
    return render_template('all_vehicles.html',
                           fengshui = fengshui, occupation = occupation, username = username)

@app.route('/down_payment_form', methods = ['GET', 'POST'])
def down_payment():
    if request.method == "POST":
        return redirect(url_for("confirmation_3"))

    vehicle_id = request.args.get('vehicle_id')
    listing_id = request.args.get('listing_id')
    return render_template('down_payment.html', vehicle_id=vehicle_id, listing_id=listing_id)

@app.route('/invoice')
def invoice():
    return render_template("invoice.html")

@app.route('/confirmation2', methods = ['GET', 'POST'])
def confirmation_2():
    return render_template('confirmation_2.html')

@app.route('/confirmation_3', methods = ['GET', 'POST'])
def confirmation_3():
    return render_template("confirmation_3.html")

if __name__ == "__main__":
    app.run(debug = True)