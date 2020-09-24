# open cv lib
import cv2
# numpy lib
import numpy as np 
import math
# matplotlib
from matplotlib import pyplot as plt 
from skimage import morphology
from skimage.feature import greycomatrix, greycoprops
from skimage import data
import skimage 

from datetime import datetime,date
import os
from app import app
from db_config import mysql

import pprint
import sys
import imutils

# fuzzyKnn algorithm
# from fuzzyknn import *
from knn import *
from knn_modify import *


class IProc:
	temp_name = {}
	# fungsi utama
	def image_process_main(self,imgname,mri_id,type_process=1):
		self.temp_name = {}
		# save to name of file
		self.temp_file_name('default',imgname)

		if type_process == 1:
			# convert grayscale
			img_gray = self.img_grayscale(imgname,mri_id)
			if img_gray!="0":

				self.temp_file_name('grayscale',img_gray)
				img_thresh = self.img_thresholding(img_gray,mri_id)

				if img_thresh!="0":

					self.temp_file_name('threshold',img_thresh)
					img_morph = self.img_morphology(img_thresh,mri_id)

					if img_morph!="0":

						self.temp_file_name('morphology',img_morph)
						img_extract = self.img_extraction(img_morph,mri_id)

						if img_extract!="0":
							datas ={"result":"1","name_of_files":self.get_temp_file(),"value_extractions":self.get_value_extractions(mri_id)} 

							return datas
						else:
							return "0"
					else:
						return "0"
				else:
					return "0"
			else:
				return "0"
		else:
			result = self.img_process_scratch(imgname,mri_id)
			return result
		




	# fungsi convert normal image to grayscale
	def img_grayscale(self,imgname,mri_id):
		# convert to grayscale
	 	img_gray = cv2.imread("static/image_resources/"+imgname,cv2.IMREAD_GRAYSCALE)
	 	# split name
	 	splitname= imgname.split('.')
	 	# new name with prefix gray
	 	newname  = str(splitname[0])+'_gray.jpg'
	 	# save as 
	 	cv2.imwrite("static/image_resources/"+newname,img_gray)

	 	# update name file to db
	 	try:
	 		sql  = "UPDATE mri_classifications_data SET image= %s WHERE mri_id =  %s"
	 		data = (newname,mri_id)
	 		conn = mysql.connect()
	 		cursor = conn.cursor()
	 		cursor.execute(sql,data) 
	 		conn.commit()
	 		return newname
	 	except Exception as e:
	 		print(e)
	 		return "0"


	def img_thresholding(self,imgname,mri_id):
		# read file
		img_gray = cv2.imread("static/image_resources/"+imgname,cv2.IMREAD_GRAYSCALE)
		# set value of thresholding
		thresh = 0
		maxValue = 255
		# convert to image threshold
		th, dst = cv2.threshold(img_gray, thresh, maxValue,cv2.THRESH_BINARY+cv2.THRESH_OTSU);
		# split name
		splitname = imgname.split("_")
		# new name
		img_thresh = str(splitname[0])+'_thresh.jpg'
		# save to another name file
		cv2.imwrite("static/image_resources/"+img_thresh,dst)

		# update name file to db
		try:
			sql  = "UPDATE mri_classifications_data SET image= %s WHERE mri_id =  %s"
			data = (img_thresh,mri_id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data) 
			conn.commit()	
			return img_thresh
		except Exception as e:
			return "0"



	def img_morphology(self,imgname,mri_id):
		# read file
		img_thresh 	= cv2.imread("static/image_resources/"+imgname,cv2.IMREAD_GRAYSCALE)
		# morphology process
		kernel 		= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
		res 		= cv2.morphologyEx(img_thresh,cv2.MORPH_OPEN,kernel)
		fills 		= morphology.remove_small_objects(res,80)
		# split name
		splitname 	= imgname.split("_")
		# newname
		img_morph   = str(splitname[0])+'_morph.jpg'

		cv2.imwrite("static/image_resources/"+img_morph,fills)
		# update name
		try:
			sql  = "UPDATE mri_classifications_data SET image= %s WHERE mri_id =  %s"
			data = (img_morph,mri_id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data) 
			conn.commit()	
			return img_morph
		except Exception as e:
			print(e)
			return "0"


	def img_extraction(self,imgname,mri_id):
		# read file
		img_morph 	= cv2.imread("static/image_resources/"+imgname,cv2.IMREAD_GRAYSCALE)
		# convert basic array to numpy array
		npar = np.asarray(img_morph)
		# glcm feature extraction process
		G = greycomatrix(npar,[1,2],[0,np.pi/2],levels=256,normed=True,symmetric=True)
		# ambil ciri
		# contrast
		contrast = greycoprops(G,'contrast')
		# dissimilarity
		dissimilarity = greycoprops(G,'dissimilarity')
		# homogeneity
		homogeneity = greycoprops(G,'homogeneity')
		# energy
		energy = greycoprops(G,'energy')
		# correlation 
		correlation = greycoprops(G,'correlation')
		# asm 
		asm = greycoprops(G,'ASM')

		# get mean of img extraction features
		mean_contrast = str(self.get_mean(contrast))
		mean_dissimilarity = str(self.get_mean(dissimilarity))
		mean_homogeneity = str(self.get_mean(homogeneity))
		mean_energy   = str(self.get_mean(energy))
		mean_correlation = str(self.get_mean(correlation))

		# update value
		try:
			sql  = "UPDATE mri_classifications_data SET contrast= %s, energy= %s, dissimilarity= %s, homogeneity= %s, correlation= %s WHERE mri_id =  %s"
			data = (mean_contrast,mean_energy,mean_dissimilarity,mean_homogeneity,mean_correlation,mri_id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data) 
			conn.commit()	
			return "1"
		except Exception as e:
			print(e)
			return "0"



	def get_mean(self,arrs):
		i = 0
		mean = 0
		subtotal =0

		for x in arrs:
			for y in x:
				subtotal+=y
				i+=1

		mean = subtotal/i

		return mean

	def temp_file_name(self,index,name_of_image):
		# self.temp_name.append(name_of_image)
		self.temp_name[index] = name_of_image


	def get_temp_file(self):
		return self.temp_name




	def get_value_extractions(self,mri_id,tipe):
		# print type(tipe)
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM mri_classifications_data WHERE mri_id = %s", (mri_id))
		row = cursor.fetchall()
		# print(row)
		value_extract = []
		feature_val = []

		
		if tipe == 2:
			for x in row:
				value_extract.append([x[2],x[3],x[4],x[5],x[6]])

			return value_extract
		else:
			for x in row:
				feature_val.append({
					"index":x[0],
					"contrast":x[2],
					"energy":x[3],
					"entropy":x[4],
					"homogeneity":x[5],
					"correlation":x[6]
					})
			return feature_val
 
		
		


	def img_process_scratch(self,imgname,mri_id):

		checkOriginImg = self.checkOriginImg(imgname)

		if checkOriginImg == 0:
			self.temp_file_name('default',imgname)
			gray = cv2.imread("static/image_resources/"+imgname)
			gray = cv2.cvtColor(gray,cv2.COLOR_RGB2GRAY)
			gray = cv2.resize(gray,(200,200))
			# split name
			splitname = imgname.split('.')
			# new name with prefix gray
			img_gray  = str(splitname[0])+'_gray.jpg'
			# save as 
			cv2.imwrite("static/image_resources/"+img_gray,gray)
			# save temp file name
			self.temp_file_name('grayscale',img_gray)
			# thresh_value = 0
			thresh_value = 153.6
			maxValue = 255
			# Basic threshold example
			th, thresh = cv2.threshold(gray, thresh_value, maxValue, cv2.THRESH_BINARY);
			img_thresh  = str(splitname[0])+'_thresh.jpg'
			# save as 
			cv2.imwrite("static/image_resources/"+img_thresh,thresh)
			# save temp file name
			self.temp_file_name('threshold',img_thresh)# morphology process
			kernel 	= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
			res 	= cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
			morph 	= morphology.remove_small_objects(res,80)
			# # new name with prefix gray
			img_morph  = str(splitname[0])+'_morph.jpg'
			# # save as 
			cv2.imwrite("static/image_resources/"+img_morph,morph)
			# # save temp file name
			self.temp_file_name('morphology',img_morph)
			# # grey = 
			PATCH_SIZE = 21
			# convert basic array to numpy array
			npar = np.asarray(morph)
			# glcm feature extraction process
			G = greycomatrix(npar,[1,2],[0,np.pi/2],levels=256,normed=True,symmetric=True)
			# ambil ciri
			# entropy
			entropy = str(skimage.measure.shannon_entropy(gray))
			# contrast
			contrast = greycoprops(G,'contrast')
			# homogeneity
			homogeneity = greycoprops(G,'homogeneity')
			# energy
			energy = greycoprops(G,'energy')
			# correlation 
			correlation = greycoprops(G,'correlation')# get mean of img extraction features
			mean_contrast = str(self.get_mean(contrast))
			# mean_dissimilarity = str(self.get_mean(dissimilarity))
			mean_homogeneity = str(self.get_mean(homogeneity))
			mean_energy   = str(self.get_mean(energy))
			mean_correlation = str(self.get_mean(correlation))
			# update value
			# pprint.pprint(contrast)
			try:
				sql  = "UPDATE mri_classifications_data SET contrast= %s, energy= %s, entropy= %s, homogeneity= %s, correlation= %s,data_type='Testing' WHERE mri_id =  %s"
				data = (mean_contrast,mean_energy,entropy,mean_homogeneity,mean_correlation,mri_id)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql,data) 
				conn.commit()	
				classification_result = self.getClassification(mri_id)		
				value_extractions= self.get_value_extractions(mri_id,1)
				self.updateData(classification_result,mri_id)
				datas ={"result":1,"name_of_files":self.get_temp_file(),"value_extractions":value_extractions,"classification_result":classification_result}			
				return datas
			except Exception as e:
				print(e)
				datas ={"result":0,"name_of_files":{},"value_extractions":{},"classification_result":"",} 
				return datas
		else:
			return {"result":2,"name_of_files":{},"value_extractions":{},"classification_result":"",} 




	def getClassification(self,mri_id):

		# get nilai ekstraksi fitur
		# tipe = 2 #tipe dari class untuk 1 == knn, 2 == knn mod
		testData = self.get_value_extractions(mri_id,tipe=2)
		knn = KNN_Mod()
		# set k
		# fuzzyknn.setK(4)
		# fuzzyknn.setK(3)
		# knn.setK(3)
		knn.getDataTraining()
		# set data testing
		knn.setTestData(testData)
		return knn.getClassification()

	def getAccuracy(self):
		knn = KNN()
		return knn.getAccuracy()
	
	def getBestK(self):
		knn = KNN()
		return knn.getBestK()
		
	def getMSEMAE(self):
		knn = KNN()
		return knn.getMSEMAE()


	def updateData(self,dataset,mri_id):


		try:
			sql  = "UPDATE mri_classifications_data SET result = %s WHERE mri_id =  %s"
			data = (dataset,mri_id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql,data) 
			conn.commit()	

			return 1

		except Exception as e:
			print(e)
			
			return 0

	def checkOriginImg(self,imgname):
		img = cv2.imread("static/image_resources/"+imgname)
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		lower_range = np.array([1,1,1])
		upper_range = np.array([255,255,255])
		mask = cv2.inRange(hsv, lower_range, upper_range)
		totalVal = 0
		for x in (mask):
			for y in (x):
				totalVal+=int(y)

		if totalVal>0:
			return 1
		else:
			return 0







