#!/usr/bin/env
import rospy
import serial
from scipy.spatial.transform import Rotation as R
from imu_driver.srv import convert, convertResponse
def callback(request):
    quadata=R.from_euler('xyz',[request.roll, request.pitch,request.yaw],degrees=True).as_quat()
    qx=quadata[0]
    qy=quadata[1]
    qz=quadata[2]
    qw=quadata[3]
    return convertResponse(qx,qy,qz,qw)

if __name__=='__main__':
    try:
        rospy.init_node("convert_to_quaternion")
        service=rospy.Service("convert_to_quaternion", convert, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    

