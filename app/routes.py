from flask import render_template,flash,redirect,url_for,request,session,abort
from app import app
from app.forms import *
import os,sys
import subprocess
from dbcode import *
import time

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

@app.route('/upload',methods=['GET','POST'])
def MainLogic():
	mainlist=[]
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		fileList = request.files.getlist('file')
		# if user does not select file, browser also
		# submit an empty part without filename
		uid=session['uid']
		for item in fileList:
			filename = secure_filename(item.filename)
			mainlist.append(filename)
			item.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			insertImages(uid , filename , app.config['UPLOAD_FOLDER']+"/"+filename)

			#time.sleep(3)
			print('inserting image ', filename)
	
		#EXECUTE_ALGO(mainlist)
	logged_in=True
	return render_template('image.html',title='Main',jumbo=False,logged_in=True)

def getList():
	fhand = open('/home/chetan/Desktop/Image-Organizer/app/imagelist.txt', 'r')
	l = list()
	for line in fhand:
		#l.append(line[:len(line) - 1])
		line = line[:len(line) - 1]
		line = line.split('/')
		l.append(line[len(line) - 1])
	print(l)
	return l

@app.route('/images',methods=['GET','POST'])
def ImagePage():
	form=SearchForm()
	if(form.validate_on_submit()):
			keyword=request.form['keyword']
			print("keyword is ",keyword)
			images_list = []
			images_list=PublicSearch(keyword)
			fhand = open('/home/chetan/Desktop/Image-Organizer/app/imagelist.txt', 'w')
			for item in images_list:
				fhand.write(item)
				fhand.write("\n")
			fhand.close()	
			flash('Search requested for user {}'.format(form.keyword.data))
			return redirect('/images')
	error=1
	return render_template('gallery.html',title='Images',form=form,images_list=getList(),error=error)




@app.route('/login',methods=['GET','POST'])
def LoginPage():
	login=False	
	form=LoginForm()
	error=None
	if(form.validate_on_submit()):
		username=request.form['username']
		password=request.form['password']
		if(SignIn(username,password)):
			session['username']=username
			session['password']=password
			flash('Login requested for user {},remember_me {}'.format(form.username.data,form.remember_me.data))
			return redirect('/upload')
		else:
			error='Invalid Credentials. Please try again.'
	return render_template('login.html',title='Login',login=False,form=form,error=error)





@app.route('/logout')
def Logout():
	#con.close()
	session.pop('username',None)
	session.pop('password',None)
	return redirect('/home')

	

@app.route('/signup',methods=['GET','POST'])
def signup():
	login=False	
	form=SignupForm()
	error=None
	if(form.validate_on_submit()):
		username=request.form['username']
		email=request.form['email']
		password=request.form['password']
		age=request.form['age']
		mobile=request.form['mobile']
		if(SignUp(username,password,email,mobile)):
			session['username']=username
			session['password']=password
			flash('Login requested for user {}'.format(form.username.data))
			return redirect('/images')
		#else:
			#error='Invalid Credentials. Please try again.'
	return render_template('signup.html',title='SignUp',login=False,form=form,error=error)


def Personal():
	pass

def EXECUTE_ALGO(image_names):
	print(image_names)
	for item in image_names:
		os.system('/home/chetan/Desktop/darknet/test.sh ' + item)
		#subprocess.call([os.path.abspath('/home/chetan/Desktop/darknet/test.sh'), image_name])
	print("dasbdsab")
	#os.system("sh /home/chetan/Desktop/darknet/test.sh image_name")
