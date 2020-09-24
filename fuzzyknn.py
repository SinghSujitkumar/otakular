from math import *
from operator import itemgetter
from app import app
from db_config import mysql

class FuzzyKNN:
	"""docstring for FuzzyKNN"""
	k_val		= ""
	m_val       = ""
	train_arr 	= None
	test_arr 	= None
	euclidean   = []
	global_arr  = None
	result_brain= []
	count_train_data = None
	count_normal_brain = 0
	count_benign_brain = 0
	count_malign_brain = 0
	NeighbourData = []
	membership_val = []


	"""set K """	
	def setK(self,k):
		self.k_val = k

	"""set M """

	def setM(self,m):
		self.m_val = -2/(m-1) 



	def showK(self):
		print (self.k_val)


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



	def getCountData(self):
		# self.count_train_data = len(self.train_arr)
		self.count_train_data = len(self.train_arr)

		for x in self.train_arr:
			if x['result'].lower() == 'normal':
				self.count_normal_brain+=1
			elif x['result'].lower() == 'benigna':
				self.count_benign_brain+=1
			else:
				self.count_malign_brain+=1

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




		# for x in self.test_arr:
		# 	dumpContrast_t.append( float(x['contrast']))
		# 	dumpEnergy_t.append( float(x['energy']) )
		# 	dumpCorrelation_t.append( float(x['correlation']) )
		# 	dumpHomogeneity_t.append( float(x['homogeneity']) )
		# 	dumpEntropy_t.append( float(x['entropy']) )


		
		# maxContrast_t 	= max(dumpContrast_t)
		# maxEnergy_t 		= max(dumpEnergy_t)
		# maxCorrelation_t 	= max(dumpCorrelation_t)
		# maxHomogeneity_t 	= max(dumpHomogeneity_t)
		# maxEntropy_t 		= max(dumpEntropy_t)

		# minContrast_t 	= min(dumpContrast_t)
		# minEnergy_t 		= min(dumpEnergy_t)
		# minCorrelation_t 	= min(dumpCorrelation_t)
		# minHomogeneity_t 	= min(dumpHomogeneity_t)
		# minEntropy_t 		= min(dumpEntropy_t)


		# dumpMinMax_t		= []

		# for x in self.test_arr:
		# 	minMaxContrast_t = (( float(x['contrast']) - minContrast_t)/(maxContrast_t-minContrast_t))
		# 	minMaxEnergy_t = ( ( float(x['energy']) - minEnergy_t)/(maxEnergy_t-minEnergy_t) )
		# 	minMaxCorrelation_t = ( ( float(x['correlation']) - minCorrelation_t)/(maxCorrelation_t-minCorrelation_t) )
		# 	minMaxHomogeneity_t = ( ( float(x['homogeneity']) - minHomogeneity_t)/(maxHomogeneity_t-minHomogeneity_t) )
		# 	minMaxEntropy_t = ( ( float(x['entropy'])-minEntropy_t)/(maxEntropy_t-minEntropy_t) )

		# 	dumpMinMax_t.append({"index":x['index'],
		# 						"contrast":minMaxContrast_t,
		# 						"energy":minMaxEnergy_t,
		# 						"correlation":minMaxCorrelation_t,
		# 						"homogeneity":minMaxHomogeneity_t,
		# 						"entropy":minMaxEntropy_t,
		# 						"result":x['result']},
		# 					)


		# self.test_arr = dumpMinMax_t




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

		for x in self.test_arr:
			print(x)


		

	def sortEuclideanDistance(self):
		temp_arr = []
		x = 1
		for y in sorted(self.euclidean, key=itemgetter('euclidean_val')):
			temp_arr.append({"index":y['index'],"euclidean_val":y['euclidean_val'],"result":y['result'],"sorted":x})
			x+=1

		self.euclidean = temp_arr

		

	def neighbour(self):
		# NeighbourData = []

		for x in self.euclidean:
			if x['sorted']<=self.k_val:
				self.NeighbourData.append({"index":x['index'],"euclidean_val":x['euclidean_val'],"result":x['result']})

				if x['result'] not in self.result_brain:
					self.result_brain.append(x['result'])


		# for x in self.result_brain:
		# 	print x
	def getMembershipFuzz(self):
		# membership_val = []
		count_data = 0
		# print(self.result_brain)/

		for i,x in enumerate(self.result_brain):
			if x == ('Normal' or 'normal'):
				count_data = float(self.count_normal_brain)
			elif x == ('Benigna' or 'benigna'):
				count_data = float(self.count_benign_brain)
			else:
				count_data = float(self.count_malign_brain)


			if i == 0:
				member_val = (0.49 * (count_data/self.count_train_data)) + 0.51
			else:
				member_val = (0.49 * (count_data/self.count_train_data))


			self.membership_val.append({"result":x,"membership_val":member_val})

	def getClassification(self):

		membership_cat  = []

		for x in self.NeighbourData:
			if x['result'] not in membership_cat:
				membership_cat.append(x['result'])


		membership_arr = []

		for x in membership_cat:
			member_root = 0
			deviation_root = 0
			for y in self.NeighbourData:
				if y['result'].lower() == x.lower():
					member_val = 1.0
				else:
					member_val = 0.0

				member_root+=(member_val * (y['euclidean_val'] ** self.m_val)) if y['euclidean_val'] > 0.00000 else  0.0
				deviation_root+=(y['euclidean_val'] ** self.m_val) if y['euclidean_val'] > 0.00000 else  0.0

			member_root_val = float(member_root/deviation_root)

			membership_arr.append({"result":x,"membership_val":member_root_val,"member_root":member_root,"deviation_root":deviation_root},)
		
		temp_arr = []
		x = 1
		for y in sorted(membership_arr, key=itemgetter('membership_val'),reverse=True):
			temp_arr.append({"membership_val":y['membership_val'],"result":y['result'],"sorted":x})
			x+=1

		max_ = temp_arr[0]["membership_val"]
		classification_result = temp_arr[0]["result"].upper()
		# print(max_)
		# print(classification_result)
		# for x in self.NeighbourData:
		# 	print(x)
		return classification_result



	# def getClassification(self):
	# 	normal_val = 0
	# 	benign_val = 0
	# 	malign_val = 0

	# 	deviation_normal_val = 0
	# 	deviation_benign_val = 0
	# 	deviation_malign_val = 0

	# 	# print(type(self.membership_val))
	# 	membership_val_normal = 0
	# 	membership_val_benign = 0
	# 	membership_val_malign = 0

	# 	for x in self.membership_val:

	# 		if x['result'].lower() == "normal":
	# 			membership_val_normal =  x['membership_val']
	# 		elif x['result'].lower() == "benigna":
	# 			membership_val_benign = x['membership_val']
	# 		else:
	# 			membership_val_malign = x['membership_val']


	# 	for i,x in enumerate(self.NeighbourData):
	# 		# print(i,self.membership_val[i])
	# 		if x['result'].lower() == "normal":
	# 			# print(x['result'])
	# 			normal_val+= ((x['euclidean_val'] * membership_val_normal) ** self.m_val) if x['euclidean_val'] > 0.0 else 0.0;
	# 			deviation_normal_val+=(x['euclidean_val'] ** self.m_val) if x['euclidean_val'] > 0.0 else 0.0;
	# 		elif x['result'].lower() == "benigna":
	# 			# print(x['result'])
	# 			benign_val+=((x['euclidean_val'] * membership_val_benign) ** self.m_val) if x['euclidean_val'] > 0.0 else 0.0;
	# 			deviation_benign_val+=(x['euclidean_val'] ** self.m_val) if  x['euclidean_val'] > 0.0 else  0.0;
	# 		else:
	# 			malign_val+=((x['euclidean_val'] * membership_val_malign) ** self.m_val) if  x['euclidean_val'] > 0.0 else 0.0;
	# 			deviation_malign_val+=(x['euclidean_val'] ** self.m_val) if  x['euclidean_val'] > 0.0 else 0.0;



		
		
		

	# 	# print(deviation_normal_val)
	# 	# print(normal_val)
	# 	# print(deviation_benign_val)
	# 	# print(benign_val)
	# 	# print(deviation_malign_val)
	# 	# print(malign_val)


	# 	normal_val = normal_val/ deviation_normal_val if normal_val > 0.0 else 0.0;
	# 	benign_val = benign_val/ deviation_benign_val if benign_val > 0.0 else 0.0;
	# 	malign_val = malign_val/ deviation_malign_val if malign_val > 0.0 else 0.0;

	# 	# print(normal_val)
	# 	# print(benign_val)
	# 	# print(malign_val)


	# 	if normal_val> benign_val and normal_val> malign_val:
	# 		# print("Normal")
	# 		return "NORMAL"
	# 	elif benign_val> normal_val and benign_val> malign_val:
	# 		# print("Benign")
	# 		return "BENIGNA"
	# 	elif malign_val> normal_val  and malign_val> benign_val:
	# 		# print("Malign")
	# 		return "MALIGNA"
	# 	else:
	# 		# print("There are same val %f %f %f " % (normal_val,benign_val,malign_val))
	# 		return "NULL"

