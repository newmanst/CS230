# Combine multiple images into one.

from __future__ import print_function
import os
import random
import csv
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.cElementTree as ET
from PIL import Image

def writeToXml(imageName, imageSize, imagePath, allCellInfo, outputFile, files):
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

  filesUsed = SubElement(root, 'files')
  # folder.text = 'WBC'
  filesUsed.text = str(files)
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

  tree = ET.ElementTree(root)
  tree.write(outputFile)


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


def combineImage(files, newImgNum):
  # Combine files into one images and save it
  result = Image.new("RGB", (640, 480))

  for index, file in enumerate(files):
    path = os.path.expanduser(file)
    img = Image.open(path)
    img.thumbnail((320, 240), Image.ANTIALIAS)
    x = index // 2 * 320
    y = index % 2 * 240
    w, h = img.size
    result.paste(img, (x, y, x + w, y + h))

  imageName = 'img_'+str(newImgNum).zfill(5)+'.jpg'
  result.save(os.path.expanduser('TEST_IMAGES/'+imageName))
  return imageName


def main():
  ''' 
  * Get all bounding boxes for each cell-type
  for nCombinedImages images:
  1) Combine image 
  2) Get all bounding boxes for image (4 per image)
  3) Create annotation
  '''
  # Create 15000 images
  nCombinedImages = 15000 # Number of created images
  nMerged = 4 # Number of augmented images merged to each combined image
  classes  = ["NEUTROPHIL", "EOSINOPHIL", "MONOCYTE", "LYMPHOCYTE"]

  bndBoxDict = {}
  bndBoxDict["NEUTROPHIL"] = getBoundingBoxes("cellbounds/cellbounds_neutrophil_test.csv")
  bndBoxDict["EOSINOPHIL"] = getBoundingBoxes("cellbounds/cellbounds_eosinophil_test.csv")
  bndBoxDict["MONOCYTE"] = getBoundingBoxes("cellbounds/cellbounds_monocyte_test.csv")
  bndBoxDict["LYMPHOCYTE"] = getBoundingBoxes("cellbounds/cellbounds_lymphocyte_test.csv")


  for i in range(nCombinedImages):
    files = []
    combinedLabels = []
    addedImages = 0
    imageSize = [640, 480]

    while addedImages < nMerged:
      imageNum = random.randint(0,3)
      cellClass = random.choice(classes)
      bndbox = bndBoxDict[cellClass][imageNum][:] # Makes copy of list to not change original values
      print("bndbox before: ", bndbox)

      # Change x-coordinates for image 2 and 3
      if(addedImages == 2 or addedImages ==3):
        bndbox[0] = str(int(bndbox[0])+imageSize[0]/2)
        bndbox[2] = str(int(bndbox[2])+imageSize[0]/2)

      # Change y-coordinates for image 1 and 3
      if(addedImages == 1 or addedImages == 3):
        bndbox[1] = str(int(bndbox[1])+imageSize[1]/2)
        bndbox[3] = str(int(bndbox[3])+imageSize[1]/2)
      
      print("Added images: ", addedImages)
      print("bndbox after: ", bndbox)

      label = [cellClass]+bndbox # Get label [class, xmin, ymin, xmax, ymax]

      # Create images
      imageFolder = 'TRAIN/'
      imageNameJPG = cellClass+'_'+format(imageNum+508, '05')+'.jpg'
      imageFileJPG = imageFolder+imageNameJPG
      if os.path.isfile(imageFileJPG):
        files.append(imageFileJPG)
        combinedLabels.append(label)
        addedImages += 1

    newImage = combineImage(files, i)
    imagePath = 'TRAIN_IMAGES/'+newImage
    labelFile = 'TRAIN_LABELS/label_'+str(i).zfill(5)+'.xml'
    writeToXml(newImage, imageSize, imagePath, combinedLabels, labelFile,files)

main()
        

    


