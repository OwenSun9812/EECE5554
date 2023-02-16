#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import bagpy
from bagpy import bagreader
import seaborn as sea
import pandas as pd


#bag = bagreader('/home/owensun/catkin_ws/src/gps_driver/data/walk.bag')
#bag = bagreader('/home/owensun/catkin_ws/src/gps_driver/data/stay.bag')
bag = bagreader('/home/owensun/catkin_ws/src/gps_driver/data/stayopen.bag')


data = bag.message_by_topic('/GPSDATA')
readings = pd.read_csv(data)


readings['utm_easting'] = readings['utm_easting'] - readings['utm_easting'].min()
readings['utm_northing'] = readings['utm_northing'] - readings['utm_northing'].min()

#readings['northing_offset'] = 
eastingmean = readings['utm_easting'].mean()
northingmean = readings['utm_northing'].mean()
readings['x_square'] = (readings['utm_northing'] - northingmean) * (readings['utm_northing'] - northingmean)
readings['y_square'] = (readings['utm_easting'] - eastingmean) * (readings['utm_easting'] - eastingmean)
readings['distance_error'] = pow((readings['x_square'] + readings['y_square']), 0.5)

errormean = readings['distance_error'].mean()
dis_std = readings['distance_error'].median()

print(readings['distance_error'].mean())
print(readings['distance_error'].median())


fig, ax = plt.subplots(figsize =(20, 14))
ax.hist(readings['distance_error'])
plt.ylabel('show times(s)')
plt.xlabel('distances error(cm)')
plt.show()
