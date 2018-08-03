#!/bin/bash
#cd /home/chetan/Desktop/darknet
cd /home/Ubuntu/darknet
./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights $1 > $2
