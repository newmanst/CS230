import os
import csv
import random
from shutil import copyfile


def labelsToDict(csvFile, originalFolder):
	reader = csv.reader(open(csvFile))
	next(reader) # skip the header
	labelDict = {'NEUTROPHIL':[], 'EOSINOPHIL':[], 'LYMPHOCYTE':[], 'MONOCYTE':[]}
	nMultiDict = {'NEUTROPHIL':0, 'EOSINOPHIL':0, 'LYMPHOCYTE':0, 'MONOCYTE':0} # Keeps track of the celltypes in multicell images

	# Populate dictionary with image numbers for each cell type
	for row in reader:
	    label = row[2].split(',')

	    # Do not use Basophil images (we have too few to get a good result)
	    if len(label) == 1 and label[0] != '' and label[0] != 'BASOPHIL':
	    	if os.path.isfile(originalFolder+'BloodImage_'+str(row[1].zfill(5))+'.jpg'): 
		    	fileNumber = row[1]
		    	labelDict[label[0]].append(fileNumber)

	    # Count number of cells of each type in multicell images
	    if len(label) == 2 and 'BASOPHIL' not in label:
	    	label = [cell.replace(' ', '') for cell in label]
	    	for cell in label:
	    		nMultiDict[cell] += 1
	return labelDict, nMultiDict

def getNumberImages(labelDict, trainSize, devSize, testSize):

	# Total number of images
	nImages = len(labelDict['NEUTROPHIL'])+len(labelDict['EOSINOPHIL'])+len(labelDict['LYMPHOCYTE'])+len(labelDict['MONOCYTE'])
	print('NEUTROPHIL', len(labelDict['NEUTROPHIL']))
	print('EOSINOPHIL', len(labelDict['EOSINOPHIL']))
	print('LYMPHOCYTE', len(labelDict['LYMPHOCYTE']))
	print('MONOCYTE', len(labelDict['MONOCYTE']))
	nTest = int(testSize*nImages/4)*4 # Number of test images (make sure it can be evenly divded by 4)
	nDev = int(devSize*nImages/4)*4 # Number of dev images (make sure it can be evenly divded by 4)
	nTrain = nImages-nTest-nDev # Number of train images
	return nTrain, nDev, nTest

def createDevSet(labelDict, nDev, originalFolder, cellTypes):
	# Get equally many random images of each celltype
	for i in range(nDev/4):
		for cellType in cellTypes:
			imageIndex = chooseImage(labelDict, cellType)
			copyImageToFolder(imageIndex, originalFolder, 'DATA_Original/DEV/'+cellType+'/')

			

def createTestSet(labelDict, nMultiDict, nTest, originalFolder, cellTypes):
	for cellType in cellTypes:
		nTestCells = nTest/4
		if(nTestCells > 0):
			for i in range(nTestCells):
				imageIndex = chooseImage(labelDict, cellType)
				copyImageToFolder(imageIndex, originalFolder, 'DATA_Original/TEST/'+cellType+'/')

def createTrainSet(labelDict, originalFolder, cellTypes):
	for cellType in cellTypes:
		for imageIndex in labelDict[cellType]:
			copyImageToFolder(imageIndex, originalFolder, 'DATA_Original/TRAIN/'+cellType+'/')


def chooseImage(labelDict, cellType):
	index = random.randint(0,len(labelDict[cellType])-1) # Get random index for this celltype
	imageIndex = labelDict[cellType].pop(index) # Get corresponding image index and remove it from dictionary
	return imageIndex
	


def copyImageToFolder(imageIndex, originalFolder, newFolder):
	imageName = 'BloodImage_'+str(imageIndex.zfill(5))+'.jpg'
	oldPath = originalFolder+imageName
	newPath = newFolder+imageName
	copyfile(oldPath, newPath)
	

def main():
	labelsFile = 'DATA_Original/labels.csv'
	originalFolder = 'OriginalNomultiImages/'
	cellTypes = ['NEUTROPHIL', 'EOSINOPHIL', 'LYMPHOCYTE', 'MONOCYTE']

	trainSize = 0.85
	devSize = 0.10
	testSize = 0.05

	labelDict, nMultiDict = labelsToDict(labelsFile, originalFolder)
	getNumberImages(labelDict, trainSize, devSize, testSize)
	nTrain, nDev, nTest = getNumberImages(labelDict, trainSize, devSize, testSize)
	print("nTrain: ", nTrain, "nDev: ", nDev, "nTest: ", nTest)
	createDevSet(labelDict, nDev, originalFolder, cellTypes)
	createTestSet(labelDict, nMultiDict, nTest, originalFolder, cellTypes)
	createTrainSet(labelDict, originalFolder, cellTypes)


main()