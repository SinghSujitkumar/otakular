from app import app
from db_config import mysql
from operator import itemgetter
# accuracy
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import os
import csv

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score,mean_squared_error,mean_absolute_error

class KNN_Mod:

	test_arr 	= None
	k_val       = None
	train_arr   = []
	result_arr  = []

	def getDataTraining(self):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT contrast, energy,entropy,homogeneity,correlation,if(result='BENIGN',1,2)result FROM mri_classifications_data")
		row = cursor.fetchall()


		for x in row:
			self.train_arr.append([x[0],x[1],x[2],x[3],x[4]]);
			self.result_arr.append(x[5])


	def setTestData(self,testData):
		self.test_arr = testData


	def setK(self,k):
		self.k_val = k


	def getK(self):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT k_val FROM setting_algorithm ")
		row = cursor.fetchall()
		self.k_val = row[0]
		# for x in row:
		# 	self.setK(x[0])


		return self.k_val



	

	def getClassification(self):
		# get K
		k = self.getK()
		print(k[0])
		knn = KNeighborsClassifier(n_neighbors=k[0],p=2)
		knn.fit(self.train_arr,self.result_arr)
		y_pred = knn.predict(self.test_arr)

		if y_pred == 1 :
			predict = "BENIGN"
		else:
			predict = "MALIGN"

		return predict

	def writeCSVData(self):
		file_name = 'brain_data.csv'
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT mri_id,contrast, energy,entropy,homogeneity,correlation,IF(result ='BENIGN',1,2)result FROM mri_classifications_data ")
		row = cursor.fetchall()

		headers = ['mri_id','contrast', 'energy','entropy','homogeneity','correlation','result']
		if os.path.isfile(file_name):
			os.remove(file_name)
			with open(file_name, mode='w') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(headers)
				writer.writerows(row)
		else:
			with open(file_name,mode='w') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(headers)
				writer.writerows(row)


	def getAccuracy(self):
		k = self.getK()

		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)

		classifier = KNeighborsClassifier(n_neighbors=k[0])
		classifier.fit(x_train,y_train)
		y_pred = classifier.predict(x_test)
		
		return accuracy_score(y_test,y_pred)
		# return " "


		# evaluating the algorithm without k fold cross validation

	def getBestK(self):
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)

		K_range = range(1,len(x_train))
		scores = {}
		scores_list = []
		for k in K_range:
			knn = KNeighborsClassifier(n_neighbors=k)
			knn.fit(x_train,y_train)
			y_pred = knn.predict(x_test)
			scores[k] = accuracy_score(y_test,y_pred)
			scores_list.append(accuracy_score(y_test,y_pred))
	
		return (K_range,scores_list)

	def getMSEMAE(self):
		k = self.getK()
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# print(brain.head())
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)

		classifier = KNeighborsClassifier(n_neighbors=k[0])
		classifier.fit(x_train,y_train)
		y_pred = classifier.predict(x_test)
			# mean error, mse, mae
		global mae,mse

		mse = mean_squared_error(y_test, y_pred)
		mae = mean_absolute_error(y_test, y_pred)

		mse = mse.astype(np.float64)
		mae = mae.astype(np.float64)
		result = {'mse': mse, 'mae': mae}
		# print(y_test)
		# print(y_pred)
		return result


	def getKFold(self):
		k = self.getK()
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# print(brain.head())
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)
		# kflod
		kf = KFold(n_splits=10,shuffle=False)
		kfold_arr = []
		i = 1
		for train_index, test_index in kf.split(x_train):

			# print("Fold ", i)
			# print("TRAIN :", train_index, "TEST :", test_index)
			# create knn model
			knn_cv = KNeighborsClassifier(n_neighbors=k[0])
			# train model with cv of 5
			cv_scores = cross_val_score(knn_cv,x_train,y_train)
			# print(cv_scores)
			# print('cv_scores mean:{}'.format(np.mean(cv_scores)))
			kfold_arr.append({"Train":train_index,"Test":test_index,"cv_scores_mean":np.mean(cv_scores)},)
			i+=1

		# print(kfold_arr)

		return ""



