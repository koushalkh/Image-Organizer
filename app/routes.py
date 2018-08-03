from flask import render_template,flash,redirect,url_for,request,session,abort
from app import app
from app.forms import *
import os,sys
import subprocess
from app.dbcode import *
import time
from random import shuffle
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
	form=SearchForm()
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
	error=None
	return render_template('gallery.html',title='Images',form=form,images_list=getList(),error=error)

def getList():
	fhand = open(os.path.abspath('app/imagelist.txt'), 'r')
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
	#if(form.validate_on_submit()):
	##if request.form['upvote']=='upvote':	
			
	#elif request.form['fav']=='fav':
	
	if request.method == 'POST':		
			keyword=request.form['keyword']
			print("keyword is ",keyword)
			images_list = []
			images_list=PublicSearch(keyword)
			fhand = open(os.path.abspath('app/imagelist.txt'), 'w')
			for item in images_list:
				fhand.write(item)
				fhand.write("\n")
			fhand.close()	
			flash('Search requested for user {}'.format(form.keyword.data))
			session['searched']=True
			return redirect('/images')
	error=1
	if session.get('logged_in')==None and session.get('searched')==None:
		random_list=fetchRandomList()
		fhand = open(os.path.abspath('app/imagelist.txt'), 'w')
		for item in random_list:
			fhand.write(item)
			fhand.write("\n")
		fhand.close()
		shuffle(random_list)
		return render_template('gallery.html',title='Images',form=form,images_list=getList(),error=error)
	else:
		return render_template('gallery.html',title='Images',form=form,images_list=getList(),error=error)

@app.route('/account',methods=['GET','POST'])
def account():
	random_list=fetchUserList()
	fhand = open(os.path.abspath('app/imagelist.txt'), 'w')
	for item in random_list:
		fhand.write(item)
		fhand.write("\n")
	fhand.close()
	shuffle(random_list)
	return render_template('account.html',title='User',images_list=getList())


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
			session['logged_in']=True
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
	session.pop('logged_in',None)
	session.pop('searched',None)
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

