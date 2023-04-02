#!/usr/bin/python3
# -*- coding: utf-8 -*-
import rospy
import serial
from imu_driver.msg import Vectornav 
from imu_driver.srv import convert,convertResponse


def imuread():





   
    
    
    msgpub = rospy.Publisher('imu', Vectornav, queue_size=10)  
    rospy.init_node('imu_Publisher', anonymous=True)
    
    port = rospy.get_param('~/imu_Publisher/port')
    #port=('/dev/ttyUSB0')
    
    ser = serial.Serial(port, 115200,timeout=1)
    
    ser.write(b'VNWRG,06,40/r/n')
    
    rospy.wait_for_service('convert_to_quaternion')
    
    
    
    
    
    
    msgpub = rospy.Publisher('imu', Vectornav, queue_size=10)  
    msg = Vectornav()
    while not rospy.is_shutdown():
        t = ser.readline().decode("utf-8").strip()
        line= str(t)
        
        if '$VNYMR' in line:
            
            word = line.split(",")
            now = rospy.get_rostime() 
            msg.header.frame_id = "imu1_frame"
            msg.header.stamp.secs = now.secs
            msg.header.stamp.nsecs = now.nsecs
            msg.raw = line
                        
            yaw = float(word[1])
            pitch = float(word[2])
            roll = float(word[3])
                            
            msg.imu.angular_velocity.x = float(word[10])
            msg.imu.angular_velocity.y = float(word[11])
            msg.imu.angular_velocity.z = float(word[12][:10])
            msg.imu.linear_acceleration.x = float(word[7])
            msg.imu.linear_acceleration.y = float(word[8])
            msg.imu.linear_acceleration.z = float(word[9])
            msg.mag_field.magnetic_field.x = float(word[4])
            msg.mag_field.magnetic_field.y = float(word[5])
            msg.mag_field.magnetic_field.z = float(word[6])
            try:
                convertimu = rospy.ServiceProxy('convert_to_quaternion', convert)
                respon = convertimu(roll,pitch,yaw)
                qx = respon.qx
                qy = respon.qy
                qz = respon.qz
                qw = respon.qw
                
            except rospy.ServiceException as e:
                print("service failed",e)

            
            msg.imu.orientation.x = qx
            msg.imu.orientation.y = qy
            msg.imu.orientation.z = qz
            msg.imu.orientation.w = qw
            print(msg.mag_field.magnetic_field.z, msg.imu.orientation.w)
            msgpub.publish(msg)   
            print(line)              

if __name__=='__main__':
    try:
        imuread()
    except rospy.ROSInterruptException:
        pass

