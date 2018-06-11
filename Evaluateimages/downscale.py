import cv2
import os

directory = 'TEST/'

for filename in os.listdir(directory):
	img = cv2.imread(directory+filename, cv2.IMREAD_UNCHANGED)
	width = int(img.shape[1] * 0.5)
	height = int(img.shape[0] * 0.5)
	dim = (width, height)
	 
	# resize image
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	cv2.imwrite('TEST_SMALL/'+filename, resized)