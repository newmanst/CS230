#! /usr/bin/env python

import argparse
import os
import numpy as np
from preprocessing import parse_annotation
from frontend import YOLO
import json

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"

argparser = argparse.ArgumentParser(
    description='Test YOLO_v2 model on any dataset')

argparser.add_argument(
    '-c',
    '--conf',
    help='path to configuration file')

argparser.add_argument(
    '-w',
    '--weights',
    help='path to pretrained weights')


def _main_(args):

    config_path = args.conf
    weights_path = args.weights

    with open(config_path) as config_buffer:    
        config = json.loads(config_buffer.read())

    ###############################
    #   Parse the annotations 
    ###############################

    # parse annotations of the test set
    test_imgs, test_labels = parse_annotation('dataset_complete/TEST_LABELS/', 
                                                'dataset_complete/TEST_IMAGES/', 
                                                config['model']['labels'])

        
    ###############################
    #   Construct the model 
    ###############################

    yolo = YOLO(backend             = config['model']['backend'],
                input_size          = config['model']['input_size'], 
                labels              = config['model']['labels'], 
                max_box_per_image   = config['model']['max_box_per_image'],
                anchors             = config['model']['anchors'])

    ###############################
    #   Load the weights
    ###############################    

    yolo.load_weights(weights_path)

    ###############################
    #   Test
    ###############################

    yolo.test(test_imgs, config['train']['batch_size'])

if __name__ == '__main__':
    args = argparser.parse_args()
    _main_(args)
