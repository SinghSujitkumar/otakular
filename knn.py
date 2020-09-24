from math import *
from app import app
from db_config import mysql
from operator import itemgetter
import statistics 

import csv 
import os
import io


# accuracy
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score,mean_squared_error,mean_absolute_error
from sklearn.neighbors import KNeighborsClassifier

# from sklearn import metrics


class KNN:
	k_val		= 1
	train_arr 	= []
	test_arr 	= []
	euclidean   = []
	result_arr  = []
	NeighbourData = []
	# x_train   = []
	# y_train   = []
	# x_test    = []
	# y_test    = []

	

	"""set K """	
	def setK(self,k):
		self.k_val = k


	def setTrainData(self):
		# self.train_arr = trainData1
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT mri_id,contrast, energy,entropy,homogeneity,correlation,result FROM mri_classifications_data WHERE data_type LIKE 'Training%' ")
		row = cursor.fetchall()
		trainData = []
		for x in row:
			trainData.append({"index":x[0],"contrast":x[1],"energy":x[2],"entropy":x[3],"homogeneity":x[4],"correlation":x[5],"result":x[6]},)
			# print(type(x[2]))
		# print(row)

		# print(trainData)
		self.train_arr = trainData


	def setTestData(self,testData):
		self.test_arr = testData



	def minMaxNormalize(self):
		dumpContrast 	= []
		dumpEnergy   	= []
		dumpCorrelation = []
		dumpHomogeneity = []
		dumpEntropy     = []

		dumpContrast_t 	= []
		dumpEnergy_t   	= []
		dumpCorrelation_t = []
		dumpHomogeneity_t = []
		dumpEntropy_t     = []

		maxContrast 	= 0.0
		maxEnergy   	= 0.0
		maxCorrelation 	= 0.0
		maxHomogeneity 	= 0.0
		maxEntropy     	= 0.0

		minContrast 	= 0.0
		minEnergy   	= 0.0
		minCorrelation 	= 0.0
		minHomogeneity 	= 0.0
		minEntropy     	= 0.0

		maxContrast_t 	= 0.0
		maxEnergy_t   	= 0.0
		maxCorrelation_t 	= 0.0
		maxHomogeneity_t 	= 0.0
		maxEntropy_t     	= 0.0

		minContrast_t 	= 0.0
		minEnergy_t   	= 0.0
		minCorrelation_t 	= 0.0
		minHomogeneity_t 	= 0.0
		minEntropy_t     	= 0.0

		for x in self.train_arr:
			dumpContrast.append( float(x['contrast']))
			dumpEnergy.append( float(x['energy']) )
			dumpCorrelation.append( float(x['correlation']) )
			dumpHomogeneity.append( float(x['homogeneity']) )
			dumpEntropy.append( float(x['entropy']) )


		
		maxContrast 	= max(dumpContrast)
		maxEnergy 		= max(dumpEnergy)
		maxCorrelation 	= max(dumpCorrelation)
		maxHomogeneity 	= max(dumpHomogeneity)
		maxEntropy 		= max(dumpEntropy)

		minContrast 	= min(dumpContrast)
		minEnergy 		= min(dumpEnergy)
		minCorrelation 	= min(dumpCorrelation)
		minHomogeneity 	= min(dumpHomogeneity)
		minEntropy 		= min(dumpEntropy)


		dumpMinMax		= []

		for x in self.train_arr:
			minMaxContrast = (( float(x['contrast']) - minContrast)/(maxContrast-minContrast))
			minMaxEnergy = ( ( float(x['energy']) - minEnergy)/(maxEnergy-minEnergy) )
			minMaxCorrelation = ( ( float(x['correlation']) - minCorrelation)/(maxCorrelation-minCorrelation) )
			minMaxHomogeneity = ( ( float(x['homogeneity']) - minHomogeneity)/(maxHomogeneity-minHomogeneity) )
			minMaxEntropy = ( ( float(x['entropy'])-minEntropy)/(maxEntropy-minEntropy) )

			dumpMinMax.append({"index":x['index'],
								"contrast":minMaxContrast,
								"energy":minMaxEnergy,
								"correlation":minMaxCorrelation,
								"homogeneity":minMaxHomogeneity,
								"entropy":minMaxEntropy,
								"result":x['result']},
							)


		self.train_arr = dumpMinMax

	def getDataTraining(self):
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT contrast, energy,entropy,homogeneity,correlation,if(result='BENIGN',1,2)result FROM mri_classifications_data")
		row = cursor.fetchall()

		for x in row:
			self.train_arr.append([x[0],x[1],x[2],x[3],x[4]]);
			self.result_arr.append(x[5])

	def euclideanDistance(self):
		

		for x in self.train_arr:
			distance = sqrt ( ( 
								(pow( (float(x['contrast']) - float(self.test_arr[0]['contrast']) ),2 )) + 
								(pow( (float(x['energy'])-float(self.test_arr[0]['energy']) ),2 ) ) + 
					   			(pow( ( float(x['correlation'])-float(self.test_arr[0]['correlation']) ) ,2 ) ) + 
					   			(pow( (float(x['homogeneity'])-float(self.test_arr[0]['homogeneity'])),2 )) +
					   			(pow( (float(x['entropy'])-float(self.test_arr[0]['entropy'])),2 ) )
					   			) 
							 )

			# print(x)

			self.euclidean.append({"index":x['index'],"euclidean_val":distance,"result":x['result']})

		# for x in self.euclidean:
			# print(x)

	def sortEuclideanDistance(self):
		temp_arr = []
		x = 1
		for y in sorted(self.euclidean, key=itemgetter('euclidean_val')):
			temp_arr.append({"index":y['index'],"euclidean_val":y['euclidean_val'],"result":y['result'],"sorted":x})
			x+=1

		self.euclidean = temp_arr

		# for x in self.euclidean:
		# 	print(x)

	def neighbour(self):
		# NeighbourData = []

		for x in self.euclidean:
			if x['sorted']<=self.k_val:
				self.NeighbourData.append({"index":x['index'],"euclidean_val":x['euclidean_val'],"result":x['result']})

				# if x['result'] not in self.result_brain:
				self.result_brain.append(x['result'])


		# for x in self.result_brain:
		# 	print(x)

	def getClassification(self):
		return statistics.mode(self.result_arr)

	classmethod
	def writeCSVData(self):
		file_name = 'brain_data.csv'
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("SELECT mri_id,contrast, energy,entropy,homogeneity,correlation,IF(result ='BENIGN',1,2)result FROM mri_classifications_data ")
		row = cursor.fetchall()
		# print(row)

		# listnya  = []
		# for x in fake_data:
			# listnya.append({x})
		headers = ['mri_id','contrast', 'energy','entropy','homogeneity','correlation','result']
		if os.path.isfile(file_name):
			# print("create")
			os.remove(file_name)
			with open(file_name, mode='w') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(headers)
				writer.writerows(row)
		else:
		# 	print("write")
			with open(file_name,mode='w') as outfile:
				writer = csv.writer(outfile)
				writer.writerow(headers)
				# for datum in fake_data:
					# writer.writerow(datum)
				writer.writerows(row)


	def getAccuracy(self):
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# print(brain.head())
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)

		classifier = KNeighborsClassifier(n_neighbors=3)
		classifier.fit(x_train,y_train)
		y_pred = classifier.predict(x_test)
		
		# print(confusion_matrix(y_test,y_pred))
		# print(classification_report(self.y_test,y_pred))
		return accuracy_score(y_test,y_pred)
		# return " "


		# evaluating the algorithm without k fold cross validation

	def getBestK(self):
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# print(brain.head())
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
		# plt.plot(K_range,scores_list)
		# plt.xlabel('Value of K for KNN')
		# plt.ylabel('Testing Accuracy')
		# plt.show()
		# print(K_range)
		# print(scores_list)
		return (K_range,scores_list)

	def getMSEMAE(self):
		self.writeCSVData()
		brain = pd.read_csv("brain_data.csv")
		# print(brain.head())
		# header delete
		X = brain.drop(["mri_id","result"],axis=1)
		# data target
		y = brain["result"]

		# train test split
		x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=4)


		classifier = KNeighborsClassifier(n_neighbors=3)
		classifier.fit(x_train,y_train)
		y_pred = classifier.predict(x_test)
			# mean error, mse, mae
		global mean_absolute_error,mean_squared_error

		mean_squared_error = mean_squared_error(y_test, y_pred)
		mean_absolute_error = mean_absolute_error(y_test, y_pred)
		result = {'mean_squared_error': float(mean_squared_error), 'mean_absolute_error': float(mean_absolute_error)}
		# print(result)
		print(y_test)
		print(y_pred)
		return result


	


