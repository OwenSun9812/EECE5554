#!/usr/bin/env python3
import bagpy
from bagpy import bagreader
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
import pandas as pd

bag = bagreader('/home/owensun/catkin_ws/src/gps_driver0/data/stay.bag')
bag.topic_table
data = bag.message_by_topic('/GPSDATA')
readings = pd.read_csv(data)
readings['altitude'] = readings['altitude'] - readings['altitude'].min()
plt.scatter(range(len(readings['altitude'])), readings['altitude'])
plt.xlabel('time(s)')
plt.ylabel('Altitude(m)')
plt.title('Station_occluded')
plt.show()
