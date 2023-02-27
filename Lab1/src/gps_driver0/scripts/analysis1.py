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
readings['altitude'] = readings['altitude'] - readings['altitude'].min()

print(readings[['altitude', 'stamp]])
print(readings)
plt.rcParams.update({'font.size': 40})
readings[['altitude','stamp]].plot()
fig, ax = bagpy.create_fig(1)
ax[0].scatter(x = 'altitude', y = 'stamp, data = readings, s= 50, label = 'altitude VS header.stamp)
for axis in ax:
    axis.legend()
    axis.set_xlabel('altitude', fontsize=40)
    axis.set_ylabel('stamp, fontsize=40)
plt.show()

