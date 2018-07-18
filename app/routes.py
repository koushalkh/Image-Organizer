import sqlite3 as sql
from flask import render_template,flash,redirect,url_for,request,session,abort
from app import app
from app.forms import LoginForm,PhotoForm
import os,sys
import subprocess

jumbo=False
login=True
from app import ALLOWED_EXTENSIONS,secure_filename

@app.route('/')
@app.route('/home')
def StartPage():
	jumbo=True
	return render_template('home.html',title='Home',jumbo=True,login=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image',methods=['GET','POST'])
def MainLogic():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			EXECUTE_ALGO(filename)
			#return redirect(url_for('/image',filename=filename))
	logged_in=True
	return render_template('image.html',title='Main',jumbo=False,logged_in=True)



@app.route('/login',methods=['GET','POST'])
def LoginPage():
	login=False	
	form=LoginForm()
	error=None
	if(form.validate_on_submit()):
		username=request.form['username']
		password=request.form['password']
		if(validate(username,password)):
			session['username']=username
			session['password']=password
			flash('Login requested for user {},remember_me {}'.format(form.username.data,form.remember_me.data))
			return redirect('/image')
		else:
			error='Invalid Credentials. Please try again.'
	return render_template('login.html',title='Login',login=False,form=form,error=error)


def validate(username,password):
	con=sql.connect('USERINFO.db')
	with con:
		print("ajdbasjbdjas")
		cur=con.cursor()
		cur.execute("SELECT * FROM USER")
		rows=cur.fetchall()
		for row in rows:
			user_name=row[0]
			pass_word=row[1]
			if(username == user_name and password == pass_word):
				print("ajdbasjbdjas")
				session['connection']=con
				return True	
	return False



@app.route('/logout')
def Logout():
	#con.close()
	session.pop('username',None)
	session.pop('password',None)
	return redirect('/home')

	

@app.route('/signup')
def signup():
	return 'SignUp'

def EXECUTE_ALGO(image_name):
	print(image_name)
	#os.system('/home/chetan/Desktop/darknet/test.sh ' + image_name)
	subprocess.call([os.path.abspath('/home/chetan/Desktop/darknet/test.sh'), image_name])
	print("dasbdsab")
	#os.system("sh /home/chetan/Desktop/darknet/test.sh image_name")