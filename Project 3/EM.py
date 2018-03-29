import numpy as np
import random
import pdb
import matplotlib.pyplot as plt
import time

class data(object):
	def __init__(self):
		self.data 	    		= None
		self.file_name  		= None
		self.mean 	    		= None
		self.covariance 		= None
		self.numberOfClusters	= None
		self.clusterProbability = None
		self.dataGivenCluster	= None
		self.clusterGivenData	= None
		self.labels				= None

	def readData(self):
		self.data = np.genfromtxt(self.file_name,delimiter=',')

	def setMean(self):
		temp = random.sample(range(self.data.shape[0]),self.numberOfClusters)
		self.mean = np.asarray([self.data[i,:] for i in temp])
	
	def setCovariance(self):
		a = np.abs(np.amin(self.data) - np.amax(self.data))
		self.covariance = np.asarray([a*np.identity(self.data.shape[1]) for i in range(self.numberOfClusters)])

class multivariateGaussian(object):	
	def getprobability(self,x,mean,sd):
		a 	= np.linalg.solve(sd,(x-mean).T).T
		b 	= (x-mean)
		pdf = np.exp(-0.5*np.sum(b*a,axis=1))/(((2*np.pi**x.shape[1])*np.linalg.det(sd))**0.5)
		return pdf

class expectation(multivariateGaussian,data):
	def __init__(self):
		data.__init__(self)

	def expect(self):
		self.dataGivenCluster = []
		for i in range(self.numberOfClusters):
			self.dataGivenCluster.append(self.getprobability(self.data,self.mean[i],self.covariance[i]))
		self.dataGivenCluster = np.asarray(self.dataGivenCluster)
		self.clusterGivenData = self.dataGivenCluster.T*self.clusterProbability
		self.clusterGivenData = self.clusterGivenData/np.sum(self.clusterGivenData,axis=1)[:,np.newaxis]
		
class maximization(multivariateGaussian,data):
	def __init__(self):
		data.__init__(self)
	
	def maximize(self):
		self.clusterProbability = np.sum(self.clusterGivenData,axis=0)/self.data.shape[0]
		self.mean = np.dot(self.clusterGivenData.T,self.data)/np.sum(self.clusterGivenData,axis=0)[:,np.newaxis]
		self.covariance = [np.dot(((self.clusterGivenData[:,i].T*(self.data-self.mean[i,:]).T)),(self.data-self.mean[i,:]))/np.sum(self.clusterGivenData,axis=0)[i] for i in range(self.numberOfClusters)]

class EM(expectation,maximization):
	def __init__(self,fileName,numberOfClusters):
		expectation.__init__(self)
		maximization.__init__(self)
		self.file_name			= fileName
		self.numberOfClusters	= numberOfClusters
		self.clusterProbability = np.ones(numberOfClusters)/numberOfClusters
		self.dataGivenCluster	= []
		self.clusterGivenData	= []
		self.logLikelihood		= [1]

	def getlogLikelihood(self):
		a = self.dataGivenCluster==0
		self.dataGivenCluster[a] = 1e-100
		self.logLikelihood.append(int(np.sum(np.log(np.sum((self.clusterProbability)*(self.dataGivenCluster).T,axis=1)))))

	def findCluster(self):
		self.readData()
		self.setMean()
		self.setCovariance()
		temp = 0
		epsilon = 1e-4
		i=0
		while abs(temp-self.logLikelihood[-1])>epsilon:
			temp = self.logLikelihood[-1]
			self.expect()
			self.maximize()
			self.getlogLikelihood()
			print(self.logLikelihood[-1])
			i+=1
	
	def findBestCluster(self):
		new = -float('Inf')
		for i in range(10):
			prev = new
			new  = self.findCluster() 
			if new>prev:
				temp_mean = np.copy(self.mean)
				temp_covariance = np.copy(self.covariance)
				temp_cgd	    = np.copy(self.clusterGivenData)
				temp_logLikelihood = np.copy(self.logLikelihood)
		self.mean = temp_mean
		self.covariance = temp_covariance
		self.clusterGivenData = temp_cgd
		self.logLikelihood = temp_logLikelihood
		plt.plot(self.logLikelihood[1:])
		plt.xlabel('number of iterations')
		plt.ylabel('Log-likelihood')
		plt.show()
		print(self.logLikelihood[-1])
	
	def visualize(self):
		b = np.argmax(self.clusterGivenData,axis=1)
		for i in range(self.data.shape[0]):
			for j in range(self.numberOfClusters):
				if b[i]==j:
					plt.plot(self.data[i,0],self.data[i,1],'C'+str(j)+'.')
		plt.show()
		plt.plot(self.logLikelihood[1:])
		plt.xlabel('number of iterations')
		plt.ylabel('Log-likelihood')
		plt.show()

if __name__ == '__main__':
	a = EM('sample EM data v2.csv',3)
	a.readData()
	start = time.time()
	a.findCluster()
	print ("Time taken is "+str(time.time()-start)+" s")
	a.visualize()