import mplleaflet as mpl
import matplotlib.pyplot as plt
import numpy as np
import math

def erroralt(altidata, mean_alt):
    erroralt = []
    for i in range(len(altidata)):
        error = altidata[i] - mean_alt
        erroralt.append(error)
    #print(erroralt)
    return erroralt
    

def errorutm(dataeast, datanorth, bad, update):
    # print(len(datanorth), len(dataeast))
    if not bad:
        X1 = np.array(datanorth[:1320])
        y1 = np.array(dataeast[:1320])
        theta1 = np.polyfit(X1, y1, 1)
        y1_line = theta1[1] + theta1[0] * X1

        X2 = np.array(datanorth[1471:2365])
        y2 = np.array(dataeast[1471:2365])
        theta2 = np.polyfit(X2, y2, 1)
        y2_line = theta2[1] + theta2[0] * X2

        X3 = np.array(datanorth[2483:3065])
        y3 = np.array(dataeast[2483:3065])
        theta3 = np.polyfit(X3, y3, 1)
        y3_line = theta3[1] + theta3[0] * X3

        X4 = np.array(datanorth[3329:])
        y4 = np.array(dataeast[3329:])
        theta4 = np.polyfit(X4, y4, 1)
        y4_line = theta4[1] + theta4[0] * X4
    elif bad and not update:
        X1 = np.array(datanorth[:1320])
        y1 = np.array(dataeast[:1320])
        theta1 = np.polyfit(X1, y1, 1)
        y1_line = theta1[1] + theta1[0] * X1

        X2 = np.array(datanorth[1471:2365])
        y2 = np.array(dataeast[1471:2365])
        theta2 = np.polyfit(X2, y2, 1)
        y2_line = theta2[1] + theta2[0] * X2

        X3 = np.array(datanorth[2034:2895])
        y3 = np.array(dataeast[2034:2895])
        theta3 = np.polyfit(X3, y3, 1)
        y3_line = theta3[1] + theta3[0] * X3

        X4 = np.array(datanorth[2742:])
        y4 = np.array(dataeast[2742:])
        theta4 = np.polyfit(X4, y4, 1)
        y4_line = theta4[1] + theta4[0] * X4
    else:
        X1 = np.array(datanorth[4:2365])
        y1 = np.array(dataeast[4:2365])
        theta1 = np.polyfit(X1, y1, 1)
        y1_line = theta1[1] + theta1[0] * X1

        X2 = np.array(datanorth[2483:3065])
        y2 = np.array(dataeast[2483:3065])
        theta2 = np.polyfit(X2, y2, 1)
        y2_line = theta2[1] + theta2[0] * X2

        X3 = np.array(datanorth[3172:4626])
        y3 = np.array(dataeast[3172:4626])
        theta3 = np.polyfit(X3, y3, 1)
        y3_line = theta3[1] + theta3[0] * X3

        X4 = np.array(datanorth[4381:] + datanorth[:5])
        y4 = np.array(dataeast[4381:] + dataeast[:5])
        theta4 = np.polyfit(X4, y4, 1)
        y4_line = theta4[1] + theta4[0] * X4
        

    X = np.concatenate((X1, X2, X3, X4))
    y = np.concatenate((y1, y2, y3, y4))
    y_line = np.concatenate((y1_line, y2_line, y3_line, y4_line))
    error_east = y - y_line
    utm_std_dev = sum(i*i for i in error_east) / len(error_east)
    print('Utm Standard Deviation: ', utm_std_dev)

    return X, y, y_line, error_east
    

def plotdatatograph(altidata, eastdata, northdata, bad, stay, process):
    

    
    avgalt = np.average(altdata)
    stddev_altitude = np.std(altdata)
    print('Altitude Average Value: ' + str(avgalt))
    print('Altitude Standard Deviation: ' + str(stddev_altitude))
    
    
    plt.figure(1)
    plt.plot(altdata, label='collection data')
    print('Max Altiude: ' + str(max(altdata)))
    print('Min Altitude: ' + str(min(altdata)))
    plt.xlabel('Data Point')
    plt.ylabel('Altitude (meters)')
    if stay:
        plt.title('Altitude for Stationary')
    else:
        plt.title( 'Altitude for Moving')
    plt.axhline(y = avgalt, color='g', label='average value')
    plt.legend()
    plt.grid(linestyle=':')

    
    plt.figure(2)
    error_alt = erroralt(altidata, avgalt)
    plt.hist(error_alt, bins=100)
    plt.ylabel('Number of Data')
    plt.xlabel('Error (meters)')
    if stay: 
        plt.title('Error of Altitude for Stationary Data' )
    else:
        plt.title('Error of Altitude for Moving Data' )
    plt.grid(linestyle=':')

   
    avgeast = np.average(eastdata)
    avgnorth = np.average(northdata)

    
    plt.figure(3)
    print('Max UTM Easting: ' + str(max(eastdata)))
    print('Min UTM Easting: ' + str(min(eastdata)))
    print('Max UTM Northing: ' + str(max(northdata)))
    print('Min UTM Northing: ' + str(min(northdata)))
    if stay:
        plt.title( 'UTM for Static graph' )
        plt.scatter(northdata, eastdata, edgecolor='tab:blue', facecolors='none', label='collection data')
        plt.plot(avgnorth, avgeast, 'ro', label='average data')
        print('UTM Easting Average: ' + str(avgeast))
        print('UTM Northing Average: ' + str(avgnorth))
    else:
        x, y, y_line, dataeast = errorutm(eastdata, northdata, bad, process)
        plt.title('UTM for Moving graph' )
        plt.scatter(x, y, label='collection data')   
        plt.plot(x, y)     
        plt.plot(x, y_line, 'b', label='Best Fit Line')
    plt.xlabel('UTM_Northing')
    plt.ylabel('UTM_Easting')
    plt.legend()
    plt.grid(linestyle=':')

   
    plt.figure(4)
    if stay:
        east_error = eastdata - avgeast
        north_error = northdata - avgnorth
        stay_error = np.sqrt(np.square(east_error) + np.square(north_error))
        for i in range(len(stay_error)):
            if north_error[i] < 0:
                stay_error[i] *= -1
        plt.hist(stay_error, bins=100)
        plt.title( 'Error of UTM for Static graph')
        plt.xlabel('Distance From Average Point (meters)')
        utm_std_dev = np.std((northdata - avgnorth, eastdata - avgeast))
        print('UTM Standard Deviation: ', utm_std_dev)
    else:
        plt.hist(dataeast, bins=100)
        plt.title('Error of UTM for Moving graph' )
        plt.xlabel('Error (meters)')
    plt.ylabel('Number of Data')
    
    plt.grid(linestyle=':')

    plt.show()


if __name__ == '__main__':
    altdata = []
    longitude_data = []
    latitude_data = []
    easting_data = []
    northing_data = []

    data_process = True
    file_name = 'tennis_moving.yaml'
    if 'isec' in file_name:
        bad_flag = True
    else:
        bad_flag = False
    if 'mov' in file_name:
        stay_flag = False
    else:
        stay_flag = True

    with open(file_name) as f:
        lines = f.readlines()

        if data_process:
            # print(len(lines))
            i = 0
            while i < len(lines):
                # print(i)
                data = lines[i]
                if 'quality' in data:
                    quality = int(data[8:])
                    # print(quality)
                    if quality == 1:
                        del_index = lines.index('quality: 1\n')
                        del lines[(del_index//16) * 16: (del_index//16 + 1) * 16]
                        i -= 16
                i += 1
                
        for line in lines:
            if 'altitude' in line:
                alt = float(line[10:])
                if alt != 0.0:
                    altdata.append(alt)

            elif 'longitude' in line:
                lon = float(line[11:])
                if lon != 0.0:
                    longitude_data.append(lon)

            elif 'latitude' in line:
                lat = float(line[10:])
                if lat != 0.0:
                    latitude_data.append(lat)

            elif 'utm_easting' in line:
                east = float(line[12:])
                if east != 0.0:
                    easting_data.append(east)

            elif 'utm_northing' in line:
                north = float(line[13:])
                if north != 0.0:
                    northing_data.append(north)

    
    f.close()
    
    # print(len(altdata))
    plotdatatograph(altdata, easting_data, northing_data, bad_flag, stay_flag, data_process)

