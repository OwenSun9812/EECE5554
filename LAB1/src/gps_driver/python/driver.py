#!/usr/bin/python3

import rospy
import utm
import serial
from gps_driver.msg import gps_msg
from std_msgs.msg import Float64, String
from math import sin, pi


if __name__ == '__main__':
    SENSOR_NAME = "gps"
    rospy.init_node('GPS_node')
    serial_p = rospy.get_param('~port','/dev/ttyUSB0')
    serial_b = rospy.get_param('~baudrate',4800)
    sampling_r = rospy.get_param('~sampling_r',5.0)
    sampling_c = int(round(1/(sampling_r*0.007913)))
    port = serial.Serial(serial_p, serial_b, timeout=3.)
    rospy.sleep(0.2)            
    rospy.logdebug("Debug completed")    
    rospy.loginfo("Publishing Data.")
   
    publisher = rospy.Publisher("/GPSDATA", gps_msg, queue_size= 10 )
    msg = gps_msg()
   
   
    try:
        while not rospy.is_shutdown():
            line = port.readline()
            
            if line.startswith(b'$GPGGA'):
                          
                    h=line.split(b",")
                    print(h)
                    
                    
                    lat = float(h[2])
                    
                    latdir = h[3]
                    
                    lon = float(h[4])
                    
                    londir = h[5]
                    
                    alti = float(h[9])
                    

                    deg_lat = int(lat) // 100
                    minut_lat = lat - 100*deg_lat
                    
                    latitude =deg_lat + minut_lat/60

                    deg_lon = int(lon) // 100
                    minut_lon = lon - 100*deg_lon
                   
                    longitude =deg_lon + minut_lon/60
                    
                    

                    if londir==b'W':
                        longitude=-longitude

                    if latdir==b'S':
                        latitude=-latitude
                    

                    Easting, Northing, Zone_Number, Zone_Letter= utm.from_latlon(latitude,longitude)
                    print(Easting, Northing, Zone_Number, Zone_Letter)
                    
                    msg.header.stamp = rospy.get_rostime()
                    
                    msg.header.frame_id = 'GPS1_Frame'
                    msg.latitude = latitude
                    msg.longitude = longitude
                    msg.utm_easting = Easting
                    msg.utm_northing = Northing
                    msg.zone = Zone_Number
                    msg.letter = Zone_Letter
                    msg.altitude = alti
                   
                    publisher.publish(msg)
            
            else:
                if line == '':
                 rospy.logwarn("No data from GPS")
                
            
            

    except rospy.ROSInterruptException:
        port.close()

