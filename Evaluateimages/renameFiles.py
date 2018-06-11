import os
from glob import glob                                                           
import cv2 

# Renames files so the new name contains the celltype
def changeName(newName, path):
	fileNumber = 508
	for filename in os.listdir(path):
		os.rename(path+filename, path+newName+'_'+str(fileNumber).zfill(5)+'.jpg')
		fileNumber += 1


def main():
	BASE_PATH = 'DATA_Original/TEST/'
	cellTypes = ['NEUTROPHIL', 'EOSINOPHIL', 'LYMPHOCYTE', 'MONOCYTE']
	for cellType in cellTypes:
		path = BASE_PATH + cellType + '/'
		changeName(cellType, path)

main()

