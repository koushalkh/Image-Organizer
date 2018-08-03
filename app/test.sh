#!/bin/bash
cd /home/chetan/Desktop/darknet
./darknet detect cfg/yolov3.cfg yolov3.weights $1 > $2
