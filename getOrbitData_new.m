tic
%TLE
%1 41783U 16059A   18093.17383152  .00000069  00000-0  22905-4 0  9992
%2 41783  98.1258 155.9141 0032873 333.2318  26.7186 14.62910114 80995
clc
clear
orbInc=  98.1258;   %inclination in degrees
meanMo = 14.62910114;   %revolutions per day
SGPdragp1 = .00000069;  % from ---First time derivative of mean motion(rad/min^2)
SGPdragp2 = 0;     % Second time derivative of mean motion (rad/min^3
SGP4dragp = .22905e-4; %Bstar
n0 = 2*pi*meanMo/1440; % Mean motion (rad/min) 
e0 = 0.0032873; % Eccentricity (0.0<=e0>=1.0)   
M0 = 26.7186*pi/180; % Mean anomaly (rad)    
w0 = 333.2318*pi/180;  % Argument of perigee (rad)  
Ohm0 = (pi/180)*155.9141; %RAAN
revNo = 8099;
i0 = pi*orbInc/180; % Inclination (rad) 
dn0 = 2*2*pi*SGPdragp1/(1440^2); % First time derivative of mean motion(rad/min^2)
ddn0 = 6*2*pi*SGPdragp2/(1440^3); % Second time derivative of mean motion (rad/min^3)
Bstar = SGP4dragp; % SGP4 type drag coefficient
t0 =0;
modTLE = [t0 dn0 ddn0 Bstar i0 Ohm0 e0 w0 M0 n0 revNo];
dT = 0:0.1:100*2*60; % in seconds 
[X, V] = sgp_new(modTLE, dT/60); 
toc
SGP = [dT; X'; V']';
clear X V dT 
dlmwrite('sgp_output.csv', SGP,'precision',12); %decide what precision you want
%var = [SGP(1,:);SGP(360*60+1,:);SGP(720*60+1,:);SGP(1080*60+1,:);SGP(1440*60+1,:)];