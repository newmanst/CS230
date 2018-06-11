# Hyperparameter sweep. We edit the config.json file. 
import numpy as np
from math import ceil
import json
import pdb
# Randomly sweep hyperparameters
n = 5

data = {
    "model" : {
        "backend":              "Tiny Yolo",
        "input_size":           416,
        "anchors":              [1.06,1.40, 1.36,1.89, 1.61,2.42, 1.93,1.85, 2.19,2.82],
        "max_box_per_image":    5,
        "labels":               ["NEUTROPHIL", "EOSINOPHIL", "LYMPHOCYTE", "MONOCYTE"]
    },

    "train": {
        "train_image_folder":   "TrainAug2Images_small/",
        "train_annot_folder":   "TrainAug2Annot_small/",

        "train_times":          1,
        "pretrained_weights":   "",
        "batch_size":           10,
        "learning_rate":        1.46e-3,
        "nb_epochs":            15,
        "warmup_epochs":        1,

        "object_scale":         15.0 ,
        "no_object_scale":      1.0,
        "coord_scale":          1.0,
        "class_scale":          1.0,

        "saved_weights_name":   "sweep_small.h5",
        "debug":                False
    },

    "valid": {
        "valid_image_folder":   "ValidAug2Images_small/",
        "valid_annot_folder":   "ValidAug2Annot_small/",

        "valid_times":          1
    }
}
batch_size = [5,8,10,16,18] #np.random.choice(range(1,64),n, replace=False)#choice([2,4,8,16,32,64],n) #random.randint(4,20,n)
print 'Batch_size: ', batch_size  
learning_rate = np.power(10,-5*np.random.rand(n))    # np.random.uniform(low=1.5e-4, high=5.5e-5, size=n) #power(10,-5*np.random.rand(n))
print 'learning_rate: ', learning_rate
object_scale = np.random.uniform(low=1, high=20, size=n) #np.random.rand(n)*20        # determine how much to penalize wrong prediction of confidence of object predictors        
print 'object_scale: ', object_scale
#no_object_scale = np.random.choice(range(1,25),n, replace=False)
#print 'no_object_scale', no_object_scale  #np.random.rand(n)*5           # determine how much to penalize wrong prediction of confidence of non-object predictors
#print 'no_object_scale', no_object_scale
#coord_scale = np.random.rand(n)*5          # determine how much to penalize wrong position and size predictions (x, y, w, h)
#print 'Coord_scale', coord_scale
class_scale = np.random.choice(range(1,25),n, replace=False) #np.random.rand(n)*5        # determine how much to penalize wrong class prediction
print 'Class_scale: ', class_scale
# Create config files
#fileID =[]
doall = False

for i in range(n):
    fileID = 'config{0}.json'.format(i+1)
#    data['train']['batch_size'] = batch_size[i]
    data['train']['learning_rate'] = learning_rate[i]
#    data['train']['object_scale'] = object_scale[i]
#    data['train']['no_object_scale'] = no_object_scale[i]
#    data['train']['coord_scale'] = coord_scale[i]
#    data['train']['class_scale'] = class_scale[i]
    data['train']["saved_weights_name"] = 'sweep_small{0}.h5'.format(i+1)         
    #pdb.set_trace()
    with open(fileID, 'w') as outfile:
        json.dump(data, outfile)
if doall: 
    for i in range(n): 
        fileID = 'config{0}.json'.format(i+1+n)
        data['train']['learning_rate'] = learning_rate[i]
        data['train']["saved_weights_name"] = 'sweep_small{0}.h5'.format(i+1+n)
        with open(fileID, 'w') as outfile:
            json.dump(data, outfile)

    for i in range(n):
        fileID = 'config{0}.json'.format(i+1+2*n)
        data['train']['object_scale'] = object_scale[i]
        data['train']["saved_weights_name"] = 'sweep_small{0}.h5'.format(i+1+2*n)
        with open(fileID, 'w') as outfile:
            json.dump(data, outfile)

    for i in range(n):
        fileID = 'config{0}.json'.format(i+1+3*n)
        data['train']['class_scale'] = class_scale[i]
        data['train']["saved_weights_name"] = 'sweep_small{0}.h5'.format(i+1+3*n)
        with open(fileID, 'w') as outfile:
            json.dump(data, outfile)
	
with open('../train_sweep.sh', 'w') as f:
    f.write('#!/bin/bash\n\n')
    for i in range(n):
        fileID = 'configs_sweep/config{0}.json'.format(i+1)       
        f.write('\n' + 'python2 train.py -c '+ fileID)


