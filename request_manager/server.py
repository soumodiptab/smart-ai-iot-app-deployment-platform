from flask import Flask, render_template, session, request, redirect, url_for, flash
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["user_db"]  # database_name
mycol = mydb["users"]  # collection_name

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
# db_user=client['users']


@app.route('/signup', methods=['POST'])
def signup():
    """Function to handle requests to /signup route."""
    if(request.method == 'POST'):
        data = request.form

        user_name = data['username']
        password = data['password']
        role = data['role']

        check_user = list(mycol.find(
            {"username": user_name}, {"_id": 0, "username": 1}))

        if(check_user != []):
            flash('User already exists', 'info')
            return redirect(url_for('login'))

        else:
            mycol.insert_one(
                {"username": user_name, "password": password, "role": role})
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def login():
    """Function to handle requests to /signin route."""
    if(request.method == 'GET'):
        return render_template('login.html')

    if(request.method == 'POST'):
        data = request.form

        username = data['username']
        password = data['password']

        check_user = list(mycol.find({"username": username}))

        if(check_user != []):
            if(check_user[0]['password'] == password):

                session['user'] = check_user[0]['username']

                if (check_user[0]['role'] == "Data Scientist"):
                    flash('Successfully logged in as Data Scientist', 'success')
                    return redirect(url_for('home'))

                elif (check_user[0]['role'] == "Application Developer"):
                    flash('Successfully logged in as Application Developer', 'success')
                    return redirect(url_for('home'))

                elif (check_user[0]['role'] == "Platform Configurer"):
                    flash('Successfully logged in as Platform Configurer', 'success')
                    return redirect(url_for('home'))

                else:
                    flash('Successfully logged in as End User', 'success')
                    return redirect(url_for('home'))

            else:
                flash('Invalid credentials', 'error')
                return redirect(url_for('login'))

        else:
            flash('User does not exist', 'info')
            return redirect(url_for('login'))


@app.route('/signout', methods=['GET'])
def logout():
    session.pop('user', None)
    flash("You have successfully logged out", "success")
    return render_template("logout.html")


@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(port=8080, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
