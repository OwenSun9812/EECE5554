#!/usr/bin/python3


import rospy
import serial
from math import sin, pi
from std_msgs.msg import Float64, String
import utm
from gnss_driver.msg import gnss
from curses.ascii import alt



def changeofunit(deg_min, deg_type):
    
    if degree_type == 'E':
        degree_decimal = float(degree_minute[:3]) + float(degree_minute[3:]) / 60
    elif deg_type == 'W':
        deg_deci = -(float(deg_min[:3]) + float(deg_min[3:]) / 60)
    elif degree_type == 'S':
        degree_decimal = -(float(degree_minute[:2]) + float(degree_minute[2:]) / 60)
    elif deg_type == 'N':
        deg_deci = float(deg_min[:2]) + float(deg_min[2:]) / 60
    else: 
        deg_deci = 0.0
    return deg_deci



if __name__ == '__main__':
    SENSOR_NAME = "gnss_gps"
    rospy.init_node('GPS_DATA')
    serial_port = rospy.get_param('~port','/dev/ttyACM0')
    serial_baud = rospy.get_param('~baudrate',57600)
    
    port = serial.Serial(serial_port, serial_baud, timeout=3.)
    
    sampling_count = int(round(1/(sampling_rate*0.007913)))
    rospy.sleep(0.2)            
    rospy.logdebug("Everything work")    
    rospy.loginfo("Publishing GNSSDATA.")
   
    pub = rospy.Publisher("GNSSDATA", gnss, queue_size= 10 )
    msg = gnss()
   
   
   
   
   
    try:
        while not rospy.is_shutdown():
            line = port.readline()
            print(line)
            if line == '':
                rospy.logwarn("No data")
            else:
            
            	   
                if line.startswith(b'$GNGGA'):
                     msg.Header.stamp=rospy.Time.now() 
                          
                 try: 
                     n = line.split(',')
                     if n[2] != '':
                          
                          msg.quality = int(n[6])
                          msg.altitude = float(n[9])
                          msg.longitude = changeofunit(n[4], n[5])
                          msg.latitude = changeofunit(n[2], n[3])
                          
                          utmmsg = utm.from_latlon(gps_msg.latitude, gps_msg.longitude)
                          msg.utm_northing = float(utmmsg[1])
                          msg.utm_easting = float(utmmsg[0])
                          
                          msg.HDOP=float(n[8])
                          
                          msg.zone = int(utmmsg[2])
                          msg.letter = str(utmmsg[3])
                          
                 pub.publish(msg)
                 rospy.loginfo(msg)


                  

            
            

    except rospy.ROSInterruptException:
        port.close()
