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


#This is the landing page
@app.route('/')
@app.route('/login')
def home_template():
    return render_template('login_radius.html')


# This page will take you to your profile page if login is successful
@app.route('/auth/login', methods= ['POST'])
def login_template():
    username = request.form['username']
    password = request.form['password']
    session = {"username": username, "password": password}
    if radius.authenticate(username=session['username'], password=session['password'], secret='LCTCS', host='ise.lctcs.edu', port=1812):
        session = {"username": request.form['username'], "password": request.form['password']}
        session['username'] = username
    else:
        session = {"username": request.form['username'], "password": request.form['password']}
        session['username'] = None

    return render_template('profile.html', username= session['username'])

# This page will allow you to enter params to configure devices
@app.route('/get/config/commands')
def get_commands():
    return render_template('get__config_commands.html')

# This page will take param entered from '/get/config/commands' to do the work of sending the config to devices and display the results
@app.route('/commands', methods= ['POST'])
def return_commands():
    address = request.form['ip_address']
    commands = request.form['commands']
    username = request.form['username']
    enable = request.form['enable']
    password = request.form['password']
    ipAddress_list = address.split(',')
    command_list = commands.split(',')
    send_config(ipAddress_list, username, password, enable, command_list)

    return render_template('commands.html', commands= command_list)


if __name__ == '__main__':
    app.run()
