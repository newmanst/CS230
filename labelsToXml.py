from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import csv
import xml.etree.cElementTree as ET
import os

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile):
	""" Makes xml-labels for one image

		Args:
		imageName: Filename of image
		imageSize: [width, height]
		imagePath: Path to image
		allCellInfo: [[name1, xmin1, ymin1, xmax1, ymax1], ..., [nameN, xminN, yminN, xmaxN, ymaxN]]
		outputFile:  xml output-file
	"""

	root = Element('annotation')
	root.set('verified', 'no')

	folder = SubElement(root, 'folder')
	folder.text = 'WBC'
	filename = SubElement(root, 'filename')
	filename.text = imageName
	path = SubElement(root, 'path')
	path.text = imagePath
	source = SubElement(root, 'source')
	database = SubElement(source, 'database')
	database.text = 'Unknown'
	size = SubElement(root, 'size')
	width = SubElement(size, 'width')
	width.text = str(imageSize[0])
	height = SubElement(size, 'height')
	height.text = str(imageSize[1])
	depth = SubElement(size, 'depth')
	depth.text = '3'
	segmented = SubElement(root, 'segmented')
	segmented.text = "0"

	for cell in allCellInfo:
	    name_str, xmin_str, ymin_str, xmax_str, ymax_str = cell
	    objectTag = SubElement(root, 'object')
	    name = SubElement(objectTag, 'name')
	    name.text = name_str
	    pose = SubElement(objectTag, 'pose')
	    pose.text = 'Unspecified'
	    truncated = SubElement(objectTag, 'truncated')
	    truncated.text = '0'
	    difficult = SubElement(objectTag, 'difficult')
	    difficult.text = '0'
	    bndbox = SubElement(objectTag, 'bndbox')
	    xmin = SubElement(bndbox, 'xmin')
	    xmin.text = xmin_str
	    ymin = SubElement(bndbox, 'ymin')
	    ymin.text = ymin_str
	    xmax = SubElement(bndbox, 'xmax')
	    xmax.text = xmax_str
	    ymax = SubElement(bndbox, 'ymax')
	    ymax.text = ymax_str

	#print prettify(root)

	tree = ET.ElementTree(root)
	tree.write(outputFile)


def getOldLabels(oldLabelFile):
	# Get old labels
	allOldLabels = []
	allImageNumbers = []
	imageNum = 0
	with open(oldLabelFile, 'r') as oldLabels:
		for line in oldLabels:
			cells = []
			thisLine = line.replace(" ", "").split(',');
			if thisLine[1].isdigit():
			  index = int(line.split(',')[1])
			  for i in range(2,len(thisLine)):
			    cells.append(thisLine[i].strip('\n').replace('"', '')) # Remove end of line and " before appening to cells
			  # Skip images with more than one cell
			  if(len(cells)==1 and cells!=['\r']):
			  	allOldLabels.append(cells)
			  	allImageNumbers.append(imageNum)
			  imageNum += 1
	return allOldLabels, allImageNumbers

def getBoundingBoxes(csvFile):
	# Get bounding boxes [xmin, ymin, xmax, ymax] for all images
	bndboxList = []
	with open(csvFile, 'r') as bFile:
		for line in bFile:
			thisLine = line.strip('\n').replace(" ", "").replace('"', '').split(',');
			bndboxList.append(thisLine)
	return bndboxList


def main():

	allOldLabels, allImageNumbers = getOldLabels('labels.csv')
	bndboxList = getBoundingBoxes('cellbounds.csv')

	# Create new labels
	nImages = len(bndboxList)
	for i in range(nImages):
		imageName = 'BloodImage_'+format(allImageNumbers[i], '05') # Do we have to add '.jpg'?
		imageSize = ['640', '480']
		imagePath = 'noMulti_Images/'+imageName+'.jpg'
		outputFile = 'wbcAnnotations/'+imageName+'.xml'

		# TODO: Make a for-loop here if we want to handle images with several cells
		classLabel = [allOldLabels[i][0].replace('\r', "")]
		bndboxLabel = bndboxList[i]
		allCellInfo = [classLabel + bndboxLabel]
		#print(allCellInfo)
		writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile)
		print(imageName, "written to", outputFile)

main()

