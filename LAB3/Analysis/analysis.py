#!/usr/bin/python3

import bagpy
import math
import csv
import statistics
from bagpy import bagreader
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.size': 16})

bag = bagreader('/home/owensun/catkin_ws/src/imu_driver/Data/record.bag')
data = bag.message_by_topic('/imu')
readings = pd.read_csv(data)
w = readings['imu.orientation.w'] * (np.pi/180)
x = readings['imu.orientation.x']* (np.pi/180)
y = readings['imu.orientation.y']* (np.pi/180)
z = readings['imu.orientation.z']* (np.pi/180)
print(w, readings['imu.orientation.w'])



t0 = +2.0 * (w * x + y * z)
t1 = +1.0 - 2.0 * (x * x + y *y)
roll_x = np.degrees(np.arctan2(t0, t1))

t2 = +2.0 * (w * y - z * x)
t2 = np.where(t2>+1.0, +1.0,t2)
t2 = np.where(t2<-1.0, -1.0,t2)
pitch_y = np.degrees(np.arcsin(t2))

t3 = +2.0 * (w * z + x * y)
t4 = +1.0 - 2.0 * (y * y+ z * z)
yaw_z = np.degrees(np.arctan2(t3, t4))

readings['Time'] = readings['Time'] - readings['Time'].min()
readings['imu.angular_velocity.x'] = readings['imu.angular_velocity.x'] - readings['imu.angular_velocity.x'].min()
readings['imu.angular_velocity.y'] = readings['imu.angular_velocity.y'] - readings['imu.angular_velocity.y'].min()
readings['imu.angular_velocity.z'] = readings['imu.angular_velocity.z'] - readings['imu.angular_velocity.z'].min()
readings['imu.linear_acceleration.x'] = readings['imu.linear_acceleration.x'] - readings['imu.linear_acceleration.x'].min()
readings['imu.linear_acceleration.y'] = readings['imu.linear_acceleration.y'] - readings['imu.linear_acceleration.y'].min()
readings['imu.linear_acceleration.z'] = readings['imu.linear_acceleration.z'] - readings['imu.linear_acceleration.z'].min()
readings['mag_field.magnetic_field.x'] = readings['mag_field.magnetic_field.x'] - readings['mag_field.magnetic_field.x'].min()
readings['mag_field.magnetic_field.y'] = readings['mag_field.magnetic_field.y'] - readings['mag_field.magnetic_field.y'].min()
readings['mag_field.magnetic_field.z'] = readings['mag_field.magnetic_field.z'] - readings['mag_field.magnetic_field.z'].min()


print('Mean & Standard Deviation of RPY:')
print('mean = ',statistics.mean(roll_x))
print('mean = ',statistics.mean(pitch_y))
print('mean = ',statistics.mean(yaw_z))
print('standard deviation = ',statistics.stdev(roll_x))
print('standard deviation = ',statistics.stdev(pitch_y))
print('standard deviation = ',statistics.stdev(yaw_z))


print('Mean & Standard Deviation of Angular Velocity:')
for i in ['imu.angular_velocity.x', 'imu.angular_velocity.y', 'imu.angular_velocity.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())



print('Mean & Standard Deviation of Linear Acceleration:')
for i in ['imu.linear_acceleration.x', 'imu.linear_acceleration.y', 'imu.linear_acceleration.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())


print('Mean & Standard Deviation of Magnetic Field:')
for i in ['mag_field.magnetic_field.x', 'mag_field.magnetic_field.y', 'mag_field.magnetic_field.z']:
    print('mean = ',readings[i].mean())
    print('standard deviation = ',readings[i].std())



x = readings['header.stamp.secs'] 
y_x = readings['imu.angular_velocity.x'] 
y_y = readings['imu.angular_velocity.y'] 
y_z = readings['imu.angular_velocity.z'] 
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])

ax.plot(x,y_x)
ax.plot(x,y_y)
ax.plot(x,y_z,'r-')

ax.legend(labels = ('x', 'y','z'), loc = 'top right')
ax.set_xlabel('Time(s)')
ax.set_ylabel('Angular Velocity(rad/sec)')
ax.set_title("Time_vs_Angular Velocity Plot")


x = readings['header.stamp.secs'] 
y_x = readings['imu.linear_acceleration.x'] 
y_y = readings['imu.linear_acceleration.y'] 
y_z = readings['imu.linear_acceleration.z'] 
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])

ax.plot(x,y_x)
ax.plot(x,y_y)
ax.plot(x,y_z,'r-')

ax.legend(labels = ('x', 'y','z'), loc = 'top right')
ax.set_xlabel('Time(s)')
ax.set_ylabel('Linear Acceleration(m/s^2)')
ax.set_title("Time_vs_LinearAcceleration Plot")





x = readings['header.stamp.secs'] 
y_x = roll_x 
y_y = pitch_y 
y_z = yaw_z
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])

ax.plot(x,y_x)
ax.plot(x,y_y)
ax.plot(x,y_z,'r-')

ax.legend(labels = ('x', 'y','z'), loc = 'top right')
ax.set_xlabel('Time(s)')
ax.set_ylabel('RollPitchYaw(degrees)')
ax.set_title("Time_vs_RollPitchYaw Plot")









f, ax = plt.subplots(3, 1, figsize=(30, 18))
f.subplots_adjust(hspace=0.4)
ax[0].hist(readings['imu.linear_acceleration.x'], bins= 40)
ax[1].hist(readings['imu.linear_acceleration.y'], bins= 40)
ax[2].hist(readings['imu.linear_acceleration.z'], bins= 40)
ax[0].set_xlabel('Linear Acceleration_X (m/s\u00b2))')
ax[0].set_ylabel('Frequency')
ax[0].set_title('Linear Acceleration_X (m/s\u00b2) vs Frequency')
ax[1].set_xlabel('Linear Acceleration_Y (m/s\u00b2))')
ax[1].set_ylabel('Frequency')
ax[1].set_title('Linear Acceleration_Y (m/s\u00b2) vs Frequency')
ax[2].set_xlabel('Linear Acceleration_Z (m/s\u00b2)')
ax[2].set_ylabel('Frequency')
ax[2].set_title('Linear Acceleration_Z (m/s\u00b2) vs Frequency')


plt.rcParams.update({'font.size': 22})
plt.show()

