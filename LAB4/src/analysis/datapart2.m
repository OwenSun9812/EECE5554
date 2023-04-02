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


alpha = 0.6;

yaw_filtered = zeros(L);
yaw_filtered(1) = 0;

for i = 1:L-1
    j = i + 1;
    yaw_filtered(j) = alpha * (yaw_filtered(i) + hpf(j) * 0.05) + (1 - alpha) * lpf(j);
end
plot(imuTime,yaw_filtered, 'LineWidth', 2);

xlabel('Time/s')
ylabel('Angle/Degree')
legend({'LPF Calibrated Yaw', 'HPF Gyro Yaw','CF'}, 'FontSize', 14);
grid on;
title('LPF for Magnetic Yaw and HPF for Gyro Yaw')







