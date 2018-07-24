#!/bin/bash
cd /home/koushal/Documents/darknet
./darknet detect cfg/yolov3.cfg yolov3.weights $1 > $2
