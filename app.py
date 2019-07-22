__author__ = "Ryan Gorden"
__email__ = "ryanw.gorden@gmail.com"


"""
This is the main applications that all modules will tie into.
The database that is being used for validating user is Cisco ISE.
The application will all user to login with there credentials
to access there profile page. From there the user will be able to
access what ever features are associated with there account. The ISE 
Database also will hold a comprehensive list of all network devices
that a user will be able to interactive with using the controller.
The main modules for this project is netmiko, flask, radius,
napalm, and requests.
"""

from flask import Flask , render_template, request
import radius

app = Flask(__name__)
app.secret_key = "Secret_key"


# This endpoint will render the login page to gather the users credentials
@app.route('/login')
def home_template():
    return render_template('login.html')




@app.route('/auth/login', methods= ['POST'])
def login_template():
    username = request.form['username']
    password = request.form['password']
    session = {"username": username, "password": password}
    if radius.authenticate(username=session['username'], password=session['password'], secret='Radius_Secret_Key', 
                           host='server_ip_or_fqdn', port=1812):
        session = {"username": request.form['username'], "password": request.form['password']}
        session['username'] = username
    else:
        session = {"username": request.form['username'], "password": request.form['password']}
        session['username'] = None

    #return username

    return render_template('profile.html', username= session['username'])

app.run(debug=True)
