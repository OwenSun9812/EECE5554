#!/usr/bin/env python3
import bagpy
from bagpy import bagreader
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
import pandas as pd

bag = bagreader('/home/owensun/catkin_ws/src/gps_driver0/data/stayopen.bag')
bag.topic_table
data = bag.message_by_topic('/GPSDATA')
readings = pd.read_csv(data)
readings['utm_easting'] = readings['utm_easting'] - readings['utm_easting'].min()
readings['utm_northing'] = readings['utm_northing'] - readings['utm_northing'].min()
print(readings[['utm_easting', 'utm_northing']])
print(readings)
plt.rcParams.update({'font.size': 40})
readings[['utm_easting','utm_northing']].plot()
fig, ax = bagpy.create_fig(1)
ax[0].scatter(x = 'utm_easting', y = 'utm_northing', data = readings, s= 50, label = 'utm_easting VS utm_northing')
for axis in ax:
    axis.legend()
    axis.set_xlabel('utm_easting', fontsize=40)
    axis.set_ylabel('utm_northing', fontsize=40)
plt.show()
