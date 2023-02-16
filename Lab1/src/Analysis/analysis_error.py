#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import bagpy
from bagpy import bagreader
import seaborn as sea
import pandas as pd


bag_file = bagreader('/home/owensun/catkin_ws/src/gps_driver/data/stayopen.bag')
bag_file = bagreader('/home/owensun/catkin_ws/src/gps_driver/data/walk.bag')
data = bag_file.message_by_topic('/GPSDATA')
readings = pd.read_csv(data)
readings['utm_easting'] = readings['utm_easting'] - readings['utm_easting'].min()
readings['utm_northing'] = readings['utm_northing'] - readings['utm_northing'].min()
readings['straightline_error'] = abs(readings['utm_northing'] - (-3 * readings['utm_easting'] + 8182))
print(readings['straightline_error'].mean())
fig, ax = plt.subplots(figsize =(20, 14))
ax.hist(readings['straightline_error'])
plt.ylabel('occuring_time(s)')
plt.xlabel('error_distances(cm)')


plt.show()
