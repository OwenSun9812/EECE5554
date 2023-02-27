#!/usr/bin/python3

import rospy
import utm
import serial
from gps_driver0.msg import gps_msg
from std_msgs.msg import Float64, String
from math import sin, pi
import argparse


if __name__ == '__main__':
    SENSOR_NAME = "gps"
    rospy.init_node("gps_Publisher", anonymous=True)
    port1 = rospy.get_param('/gps_Publisher/port')
    port = serial.Serial(port1, 4800, timeout = 1)
    publisher = rospy.Publisher("/gps", gps_msg, queue_size= 10 )
    msg = gps_msg()
   
   
    try:
        while not rospy.is_shutdown():
            line = port.readline()
            
            if line.startswith(b'$GPGGA'):
                          
                    x=line.split(b",")

                        
                    time=float(x[1])
                    
                    lat = float(x[2])
                    
                    latdir = x[3]
                    
                    lon = float(x[4])
                    
                    londir = x[5]
                    
                    alti = float(x[9])
                    utc_hrs = time//10000
                    utc_min = (time-(utc_hrs*10000))//100
                    utc_sec = (time - (utc_hrs*10000) - (utc_min*100))
                    utc_final_secs = (utc_hrs*3600 + utc_min*60 + utc_sec)
                    utc_final_nsecs = int((utc_final_secs * (10**7)) % (10**7))

                    deg_lat = int(lat) // 100
                    minut_lat = lat - 100*deg_lat
                    
                    latitude =deg_lat + minut_lat/60

                    deg_lon = int(lon) // 100
                    minut_lon = lon - 100*deg_lon
                   
                    longitude =deg_lon + minut_lon/60
                    
               

                    if latdir==b'S':
                        latitude=-latitude
                    

                    if londir==b'W':
                        longitude=-longitude
                    

                    Easting, Northing, Zone_Number, Zone_Letter= utm.from_latlon(latitude,longitude)
                    print(Easting, Northing, Zone_Number, Zone_Letter)
                    
                    msg.Header.stamp.secs = int(utc_final_secs)
                    msg.Header.stamp.nsecs = int(utc_final_nsecs)
                    
                    msg.Header.frame_id = "GPS1_Frame"
                    msg.latitude = latitude
                    msg.longitude = longitude
                    msg.utm_easting = Easting
                    msg.utm_northing = Northing
                    msg.zone = Zone_Number
                    msg.letter = Zone_Letter
                    msg.altitude = alti
                    msg.HDOP = float(x[8])
                    publisher.publish(msg)
            
            else:
                if line == '':
                 rospy.logwarn("No data from GPS")
                
            
            

    except rospy.ROSInterruptException:
        port.close()

