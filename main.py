import hashlib
from app import app
from flask import Flask,flash, render_template, request, redirect, url_for,session 
from db_config import mysql
from werkzeug import generate_password_hash, check_password_hash
# datetime
from datetime import datetime
# image pillow

# set uploading file
import os
# random number
import random
from werkzeug.utils import secure_filename
# image processing lib
from iproc import *
from knn_modify import *
from knn import *


# path
import os,glob
import os.path

#set uploading folder
UPLOAD_FOLDER = 'static/image_resources'
ALLOWED_EXTENSIONS = set(['jpg','jpeg'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	# jika statusnya sudah login
	# reset session dan redirect ke logout
	if 'logged_in' in session:
		return redirect('/logout')

	return render_template('login.html')


# fungsi untuk proses login
@app.route('/login',methods=['POST'])
def login_process():
	if 'logged_in' in session:
		return redirect('home')
	else:
		_username 			= request.form['username']
		_password 			= request.form['password']
		_hashed_password 	= hashlib.md5(_password.encode())
		conn 				= mysql.connect()
		cursor 				= conn.cursor()
		cursor.execute("SELECT * FROM user WHERE (username = %s or email = %s ) and password=%s",(_username,_username,_hashed_password.hexdigest()))
		row 				= cursor.fetchone()
		
		if row:
			count_all_data = getSpecificData(1,"")
			session['logged_in'] = True
			session['fullname']= row[1]
			session['user_id'] = row[0]
			session['type_user'] = row[6]
			session['countalldata'] = count_all_data[0]
			 
			return redirect('/home')
		else:
			session['logged_in'] = False
			flash('Maaf username atau password salah !!','danger')
			return redirect('/')

		cursor.close()
		conn.close()
		flash('Gagal Login','danger')
		return redirect('/')


# fungsi untuk kehalaman dashboard
@app.route('/home')
def home():
	if 'logged_in' in session:
		count_data_train = getSpecificData(2,"Training")
		count_data_test = getSpecificData(2,"Testing")
		
		return render_template('admin/dashboard.html',countdatatrain=count_data_train[0],countdatatest=count_data_test[0])
	else:
		flash('Anda Belum Login','danger')
		return redirect('/')


# fungsi untuk register akun
@app.route('/signup')
def register():
	return render_template('signup.html')


# fungsi untuk proses register akun
@app.route('/register_process',methods=['POST'])
def process():
	_fullname   = request.form['fullname']
	_username   = request.form['username']
	_email      = request.form['email']
	_password   = request.form['password']
	_repassword = request.form['repassword']


		# check username in db
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM user where  username=%s or email=%s",(_username,_email))
	row = cursor.fetchone()

	if row:
		flash('Maaf username atau email sudah digunakan','info')
		return redirect('/signup')
	else:
			# print("berhasil")
		if _fullname and _username and _email and  _password == _repassword and request.method == 'POST':
			_hashed_password = hashlib.md5(_password.encode())
			sql 	= "INSERT INTO user (name,username,email,password,type_user_id) VALUES (%s,%s,%s,%s,%s)"
			data 	= (_fullname,_username,_email,_hashed_password.hexdigest(),'2',)
			conn 	= mysql.connect()
			cursor 	= conn.cursor()
			cursor.execute(sql,data) 
			conn.commit()
			flash('Register successfully','success')
			return redirect('/signup')
		elif _password != _repassword and request.method =='POST':
			flash('Password tidak sama','danger')
			return redirect('/signup')
		else:
			flash('Register failed','danger')
			return redirect('/signup')
		cursor.close()
		conn.close()





# fungsi tampilan upload mri
@app.route('/upload_mri')
def view_mri():
	return render_template('admin/upload_mri.html')


# set allowed file
def allowed_file(filename):
	return '.' in filename and \
	filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



# fungsi untuk upload image
@app.route('/upload_process', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		if 'mri_file' not in request.files:
			flash('No file Part','warning')
			return redirect('/upload_mri')
		file = request.files['mri_file']

		if file.filename == '':
			flash('No selected file','danger')
			return redirect('/upload_mri')
		if file and allowed_file(file.filename):
			
			filename = secure_filename(file.filename)
           	 
			# get datetime
			timenow = datetime.now()
			# newname file
			newname = str(timenow.year)+''+str(timenow.month)+''+str(timenow.day)+''+str(timenow.hour)+''+str(timenow.minute)+''+str(timenow.second)
			# save to folder
			if file.save(os.path.join(app.config['UPLOAD_FOLDER'],newname+'.jpg')):
				print("Gagal")
				flash('Failed save to folder','danger')
				return redirect('/upload_mri')
			else:
				return redirect('/save_img_to_db/'+(newname+'.jpg'))
		else:
			flash('File is not allowed !!','danger')
			return redirect('/upload_mri')


# fungsi untuk menyimpan citra ke database
@app.route('/save_img_to_db/<imgname>')
def save_img(imgname):
	# return imgname
	if imgname != None:
		_user_id= session['user_id']
		sql 	= "INSERT INTO mri_classifications_data (image,user_id) VALUES (%s,%s)"
		data 	= (imgname,_user_id)
		conn 	= mysql.connect()
		cursor 	= conn.cursor()
		cursor.execute(sql,data) 
		mri_id 	= cursor.lastrowid
		conn.commit()
		# img processing 
		iproc = IProc()
		# image processing save
		result = iproc.image_process_main(imgname,mri_id,type_process=2)

		if result['result'] == 1:
			flash('berhasil','success')
		elif result['result'] == 2:
			# jika gambar bukan citra mri
			msg = process_deleting(mri_id,imgname)
			flash('Image File is not MRI Image','danger')
		else:
			flash('gagal','danger')

		return render_template('admin/upload_mri.html',datas=result['name_of_files'],extract=result['value_extractions'],classification_result=result['classification_result'])
		


@app.route('/getClassificationData')
def getClassificationData():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT *,mcd.mri_id mcd_id FROM mri_classifications_data mcd JOIN user u on u.user_id=mcd.user_id")
	row = cursor.fetchall()
	
	return render_template('admin/classification_data.html',data=row)
  

@app.route('/getSpecificData/<int:tipe>/<datatype>')
def getSpecificData(tipe,datatype):
	conn = mysql.connect()
	cursor = conn.cursor()
	if tipe == 1:
		cursor.execute("SELECT count(*) FROM mri_classifications_data ")
	else:
		cursor.execute("SELECT count(*) FROM mri_classifications_data where data_type LIKE %s ",(datatype))
	row = cursor.fetchone()
	return row




@app.route('/deleteMRI/<int:id>')
def deleteMRI(id):
	
	conn 		= mysql.connect()
	cursor 		= conn.cursor()
	cursor.execute("SELECT * FROM mri_classifications_data WHERE mri_id = %s",(id))
	row 		= cursor.fetchone()
	mri_id 		= row[0]
	img_name 	= row[1].split(".")
	
	msg 		= process_deleting(mri_id,img_name[0])
	flash(msg,'success')
	return redirect('/getClassificationData')



@app.route('/process_deleting/<int:mri_id>/filename')
def process_deleting(mri_id,filename):

	sql = "DELETE FROM mri_classifications_data WHERE mri_id = %s"
	data = (mri_id)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql,data) 
	conn.commit()

	# directory file
	cur_dir = "static/image_resources/"
	
	# loop file with like same name
	for file in os.listdir(cur_dir):
		if file.startswith(filename):
			# if found file will be delete
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'],file))

	return "Files has been deleted"


@app.route('/getAccuracy')
def getAccuracy():
	knn = KNN_Mod()
	
	error = knn.getMSEMAE()
	bestK = knn.getBestK()

	legend_Ac= "Akurasi, MSE dan MAE"
	labels_Ac= ["Akurasi","MSE","MAE"]
	values_Ac= [(knn.getAccuracy()*100),(error['mse']*100),(error['mse']*100)]
	
	legend_K = "Best K"
	labels_K = bestK[0]
	values_K = bestK[1]
	return render_template('admin/accuracy.html',values_K=values_K,labels_K=labels_K,legend_K=legend_K,values_Ac=values_Ac,labels_Ac=labels_Ac,legend_Ac=legend_Ac)

@app.route('/getBestK')
def getBestK():
	knn 	= KNN_Mod()
	bestK 	= knn.getBestK()
	return (str(bestK[0]))


@app.route('/getError')
def getMSEMAE():
	knn 	= KNN_Mod()
	return (str(knn.getMSEMAE()))

@app.route('/getKFold')
def getKFold():
	knn 	= KNN_Mod()
	return knn.getKFold()


# @app.route('/get')

@app.route('/setK')
def setK():
	if 'logged_in' in session:
		return render_template('admin/setK.html')
	else:
		return redirect('/logout')


@app.route('/updateK',methods=['POST'])
def updateK():
	_k_val   = request.form['k']

	sql = "UPDATE setting_algorithm set k_val=%s WHERE algo_id=1"
	data = (_k_val)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql,data) 
	conn.commit()
	flash('K Berhasil diubah','success')
	return redirect('/setK')



# change password
@app.route('/changePassword')
def changePassword():
	if 'logged_in' in session:

		return render_template('/admin/change_password.html')
	else:
		flash('Anda Belum Login !!!')
		return redirect('/')



# process update password
@app.route('/updatePassword', methods=['POST'])
def updatePassword():
	if 'logged_in' in session:
		pst = request.form

		old_password      = hashlib.md5(pst['old_password'].encode()).hexdigest()
		new_password      = pst['new_password']
		conf_new_password = pst['conf_new_password']

		# get old password
		user_id = session['user_id']
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM user WHERE user_id = %s",(user_id))
		row = cursor.fetchone()
		old_password_db = row[4]


		# jika password lama sama
		if old_password_db == old_password:
			# bandingkan password baru
			if new_password == conf_new_password:
				# convert new password to md5
				new_password = hashlib.md5(new_password.encode()).hexdigest()
				# update to db
				sql = "UPDATE user set password=%s WHERE user_id=%s"
				data = (new_password,user_id)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql,data) 
				conn.commit()
				flash('Password Berhasil diubah','success')
				return redirect('/changePassword')

			else:
				flash('Password Baru Tidak sama !!','danger')
				return redirect('/changePassword')
		#jika password lama tidak sama 
		else:
			flash('Password Lama salah !!','danger')
			return redirect('/changePassword')




		# bandingkan password lama dan password baru
		new_password = hashlib.md5(pst['new_password'].encode())
		return ""

	else:
		flash('Anda Belum Login !!!')
		return redirect('/')


# fungsi untuk logout
@app.route('/logout')
def logout():
	# update last login
	# print(session['user_id'])
	if 'user_id' in session:
		_last_login = datetime.now()
		_user_id    = session['user_id']
		sql = "UPDATE user SET last_login= %s WHERE user_id =  %s"
		data 		= (_last_login,_user_id)
		conn 		= mysql.connect()
		cursor 		= conn.cursor()
		cursor.execute(sql,data) 
		conn.commit()

	# unset session
	session.pop('logged_in',None)
	session.pop('fullname','')
	session.pop('user_id','')

	return redirect('/')


if __name__ == "__main__":
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug = True)
