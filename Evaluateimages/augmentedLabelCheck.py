import cv2
import os


def getBoundingBoxes(csvFile):
  # Get bounding boxes [xmin, ymin, xmax, ymax] for all images
  bndboxList = []
  lineNum = 0
  with open(csvFile, 'r') as bFile:
    for line in bFile:
      thisLine = line.strip('\n').replace(" ", "").replace('"', '').split(',');
      bndboxList.append(thisLine)
      lineNum += 1
  return bndboxList


bndBoxDict = {}
bndBoxDict["NEUTROPHIL"] = getBoundingBoxes("cellbounds/cellbounds_neutrophil_dev.csv")
bndBoxDict["MONOCYTE"] = getBoundingBoxes("cellbounds/cellbounds_monocyte_dev.csv")
bndBoxDict["EOSINOPHIL"] = getBoundingBoxes("cellbounds/cellbounds_eosinophil_dev.csv")
bndBoxDict["LYMPHOCYTE"] = getBoundingBoxes("cellbounds/cellbounds_lymphocyte_dev.csv")

imagePath = "DEV/"
newImagePath = "LabelCheckDev/"

for image in os.listdir(imagePath):
	cellType = image[:image.find("_")].upper()
	index = int(image[image.find("_")+1:image.find(".")])-500
	bndBox = bndBoxDict[cellType][index][:]
	xmin, ymin, xmax, ymax = map(int, bndBox)

	img = cv2.imread(imagePath+image,cv2.IMREAD_COLOR)
	cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (255,0,0), 3)
	cv2.putText(img, cellType,(xmin, ymin - 13), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
	cv2.imwrite(newImagePath+image, img)

