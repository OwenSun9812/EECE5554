clc
clear 
clf
close all 

imudataTable = readtable('imu.csv');
imuTime=(table2array(imudataTable(:,1)));
imuTime=imuTime-imuTime(1);
imuQuat = table2array(imudataTable(:,11:14));
imuGyr = table2array(imudataTable(:,16:18));
imuAcc = table2array(imudataTable(:,20:22));
imuMag = table2array(imudataTable(:,28:30));

gpsdataTable = readtable('gps.csv');
gpsTime=(table2array(gpsdataTable(:,1)));
gpsTime=gpsTime-gpsTime(1);
lat = table2array(gpsdataTable(:,6));
lon = table2array(gpsdataTable(:,7));

L = size(imuTime);


x = imuMag(13000:18000,1);
y = imuMag(13000:18000,2);
z = imuMag(13000:18000,3);

x_avg = mean(x);
y_avg = mean(y);
z_avg = mean(z);

x_radius = x - x_avg;
y_radius = y - y_avg;
z_radius = z - z_avg;

max_radius = max([max(x_radius), max(y_radius), max(z_radius)]);

x_scale = max_radius / mean(abs(x_radius));
y_scale = max_radius / mean(abs(y_radius));
z_scale = max_radius / mean(abs(z_radius));

R = diag([x_scale, y_scale, z_scale]);
R(1,3) = -x_avg*x_scale;
R(2,3) = -y_avg*y_scale;
R(3,3) = -z_avg*z_scale;

m_corr =( [x y z] -[x_avg y_avg z_avg])*R;
figure('Position', [0 0 800 800]);
plot(x,y,'LineWidth',2)
hold on
grid on
xlabel('Mag_x')
ylabel('Mag_y')
plot(m_corr(:,1),m_corr(:,2),'LineWidth',2)
legend('Before calibration','After calibration')

imuMag=imuMag-[x_avg y_avg z_avg];
imuMagCal=(imuMag)*R';
figure('Position', [100 100 800 800]);
for i = 1:3
    subplot(3, 1, i, 'position', [0.1 (i-1)*0.25+0.05 0.8 0.2])
end



intYaw = cumtrapz(imuTime,imuGyr(:,3));
yawCal = unwrap( atan2(imuMagCal(:,1),imuMagCal(:,2)));
yawRaw = unwrap( atan2(imuMag(:,1),imuMag(:,2)));



[b, a] = butter(3, 0.1/40, 'low');
lpf = filtfilt(b, a, yawCal);
[b, a] = butter(3, 0.00001/40, 'high');
hpf = filtfilt(b, a, intYaw);
figure('Position', [0 0 800 400]);
plot(imuTime,lpf, 'LineWidth', 2);
hold on;
plot(imuTime,hpf, 'LineWidth', 2);


figure('Position', [0 0 800 400]);
RPY = quat2eul(imuQuat);
plot(imuTime,intYaw,'LineWidth',2)
hold on
plot(imuTime,yawCal,'LineWidth',2)
plot(imuTime,yaw_filtered,'LineWidth',2)
plot(imuTime,unwrap(RPY(:,3)),'LineWidth',2)
grid on
legend('Yaw Integrated from Gyro','Magnetometer','Complementary filter','Yaw angle computed by the IMU', 'FontSize', 14);
xlabel('Time/s')
ylabel('Angle/Degree')

raw_val = imuAcc(:,1);
x = mean(raw_val(13000:18000));
linear_acc = raw_val - x;

difference = [];
for i = 1:(length(linear_acc)-1)
difference(i,1) = [(linear_acc(i+1) - linear_acc(i)) /(imuTime(i+1)-imuTime(i))];
end


final = linear_acc(2:end) - difference;
Forward_velocity_adjusted = cumtrapz(imuTime,linear_acc)-10;
Forward_velocity_adjustedtemp = Forward_velocity_adjusted;
Forward_velocity_adjusted(Forward_velocity_adjusted<0) = 0;
Forward_velocity_raw = cumtrapz(imuTime,raw_val);

time = gpsTime;
UTMeast = gpsdataTable.('UTM_easting');
UTMnorth =  gpsdataTable.('UTM_northing');
Latitude =gpsdataTable.('Latitude'); 
Longitude = gpsdataTable.('Longitude');
distance = [];
velocity = [];
for i = 1:(length(UTMnorth)-1)
distance(i,1) = [ sqrt(((UTMnorth(i+1) - UTMnorth(i))^2) + ((UTMeast(i+1) - UTMeast(i))^2))];
end

gps_vel = distance ./ diff(time);


figure('Position',[0 0 1200 600]);

plot(gpsTime(2:end), gps_vel, 'LineWidth', 2, 'DisplayName', 'GPS adjusted Velocity');
hold off;
legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Velocity estimate from the GPS', 'FontSize', 16);
xlabel('Time (secs)', 'FontSize', 14);
ylabel('Velocity (m/sec)', 'FontSize', 14);

set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);

figure('Position',[0 0 1200 600]);
hold on;
plot(imuTime, Forward_velocity_raw, 'LineWidth', 2, 'DisplayName', 'IMU Raw Velocity');
 plot(imuTime, Forward_velocity_adjusted, 'LineWidth', 2, 'DisplayName', 'IMU Adjusted Velocity');

legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Forward velocity from IMU and GPS before adjustment', 'FontSize', 16);
xlabel('Time (secs)', 'FontSize', 14);
ylabel('Velocity (m/sec)', 'FontSize', 14);

set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);

figure('Position',[0 0 1200 600]);
hold on;
plot(imuTime, Forward_velocity_adjusted, 'LineWidth', 2, 'DisplayName', 'IMU Adjusted Velocity');
plot(gpsTime(2:end), gps_vel, 'LineWidth', 2, 'DisplayName', 'GPS Raw Velocity');
legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Forward velocity from IMU before and after adjustment', 'FontSize', 16);
xlabel('Time (secs)', 'FontSize', 14);
ylabel('Velocity (m/sec)', 'FontSize', 14);

set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);

imuDis = cumtrapz(imuTime,Forward_velocity_adjusted);
gpsDis = cumtrapz(gpsTime(2:end),distance);

figure('Position',[0 0 1200 600]);
hold on;
plot(imuTime, imuDis, 'LineWidth', 2, 'DisplayName', 'IMU Calculated Displacement');
plot(gpsTime(2:end), gpsDis, 'LineWidth', 2, 'DisplayName', 'GPS Calculated Displacement');
legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Displacement from IMU and GPS before adjustment', 'FontSize', 16);
xlabel('Time (secs)', 'FontSize', 14);
ylabel('Displacement m', 'FontSize', 14);

set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);


x1dot = Forward_velocity_adjusted;
angz =imuGyr(:,3);
y2dot = angz(1:end) .* x1dot;
Y_observed = imuAcc(:,2);
figure('Position',[0 0 800 800]);
plot(imuTime,Y_observed, 'LineWidth', 2, 'DisplayName', 'Y observed');
hold on;
plot(imuTime,y2dot, 'LineWidth', 2, 'DisplayName', 'wX(dot)');

legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Y observed V/S wX(dot)', 'FontSize', 16);
xlabel('Samples @ 40Hz', 'FontSize', 14);
ylabel('Acceleration', 'FontSize', 14);
set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);

[b, a] = butter(3, 1/40, 'low');
Y_observedfilted = filtfilt(b, a, Y_observed);
figure('Position',[0 0 800 800]);
plot(imuTime,Y_observedfilted, 'LineWidth', 2, 'DisplayName', 'Y observed lpf');
hold on;
plot(imuTime,y2dot, 'LineWidth', 2, 'DisplayName', 'wX(dot)');
legend('FontSize', 12, 'Location', 'NorthWest');
grid on;
title('Y observed after lpf V/S wX(dot)', 'FontSize', 16);
xlabel('Time/s', 'FontSize', 14);
ylabel('Acceleration', 'FontSize', 14);
set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);

yaw_z = intYaw;
fv = unwrap(Forward_velocity_adjusted);

mgh1 = (RPY(:,3));
mgh1 = wrapToPi(yaw_z);
rot = (-108.*pi/180);

unit1 = cos(mgh1+rot).*fv;
unit2 = -sin(mgh1+rot).*fv;
unit3 = cos(mgh1+rot).*fv;
unit4 = sin(mgh1+rot).*fv;
rads = (180/pi);
ve = unit1+unit2;
vn = unit3+unit4;
xe = cumtrapz(imuTime,ve);
xn = cumtrapz(imuTime,vn);
rotxexn = [xe xn]*[-1 0;0 -1];
xe = rotxexn(1:18000,1);
xn = rotxexn(1:18000,2);
scale1 =range(UTMeast)/ range(xe);
scale2 =range(UTMnorth)/ range(xn);
xe = xe*scale1;
xn=xn*scale2;
figure('Position',[0 0 800 800]);

plot(xe-mean(xe),xn-mean(xn), 'LineWidth', 2);
hold on
grid on;
title('Trajectory of Vehicle', 'FontSize', 16);
xlabel('Xe', 'FontSize', 14);
ylabel('Xn', 'FontSize', 14);
set(gca, 'FontSize', 12);
set(gca, 'GridLineStyle', '--');
set(gca, 'GridColor', [0.5 0.5 0.5]);
set(gca, 'LineWidth', 1);
plot(UTMeast-mean(UTMeast), UTMnorth-mean(UTMnorth), 'LineWidth', 2);
grid on;
legend('IMU Calculated Trajectory','GPS Calculated Trajectory')



