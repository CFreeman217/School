% MRAC Parachute Test/Sim %
clear all
close all
clc

% Model used for simulation
T_hat = [-1.1944; 9.3192; -0.2790; -0.0244]; 
% X = [bias, input, indot, outdot]
% Input goes from -0.5 to 0.5 or so

Tf = 100;
dt = 0.01;
N = round(Tf/dt); % Length of simulation

fc = 2; % low pass filter cutoff freq for reference model
fs = 100; % sampling freq
%[b,a] = butter(2,fc/fs); % 2nd order filter model
gam = tan(pi*fc/fs);
D = gam^2 + sqrt(2)*gam + 1;
b(1) = gam^2/D;
b(2) = 2*b(1);
b(3) = b(1);
a(2) = 2*(gam^2 - 1)/D;
a(3) = (gam^2 - sqrt(2)*gam + 1)/D;

L(1) = 0.2;
L(2) = 0.2; % Two learning/adaption gains

roll_m(1:3) = 0;
roll_d(1:3) = 0;%01101101

p(1) = 0.1;
p(2) = 0;

kp = 1;
ki = 0;%0.02;

roll(1) = 0; % yaw position (angle)
rollrate(1) = 0; % Initialize yaw rate
rollaccel(1) = 0; % second derivative of yaw position (acc)
e_sum = 0; % outer loop error integral
roll_d(1) = 0; % desired yaw position

for i = 2:N
    roll_m(3) = roll_m(2);
    roll_m(2) = roll_m(1);
    roll_d(3) = roll_d(2);
    roll_d(2) = roll_d(1);
    
    % set desired
    %y_d(1) = 1*sin(2*pi*0.3*i*dt); % Oscillating desired yaw rate
    if mod(i,1000) == 0
      roll_d(1) = roll_d(1) + 1;
    else
      roll_d(1) = roll_d(1);
    end

    % error terms for outer loop
    e_sum = e_sum + (roll_d(1) - roll(i-1))*dt;
    % outer loop control law
    roll_d(1) = kp*(roll_d(1) - roll(i-1)) + ki*e_sum;
    % outer_error = yaw_des - yaw;
    % outer_error_sum = outer_error_sum + outer_error*dt_control;
    % yaw_rate_des = kp_rate * outer_error + ki_rate * outer_error_sum;
    
    % not needed
    err(i) = roll_d(1) - roll(i-1);
    
    % Running through butterworth filter for reference model
    roll_m(1) = -a(2)*roll_m(2) - a(3)*roll_m(3) + b(1)*roll_d(1) + b(2)*roll_d(2) + b(3)*roll_d(3);
    % yaw_rate_model = filter(yaw_rate_desired)

    % MRAC control law
    u(i) = p(1)*roll_d(1) + p(2); % Control law
    % cmd = gain1 * derivative of yaw desired + gain2

    % only needed for simulation model
    ud(i) = (u(i) - u(i-1))/dt;
    rollrate(i) = T_hat(1) + T_hat(2)*u(i) + T_hat(3)*ud(i) + T_hat(4) + randn(1)*0.5;
    roll(i) = roll(i-1) + rollrate(i)*dt;
    rollaccel(i) = (rollrate(i) - rollrate(i-1))/dt; % acceleration estimate
    
    % rate of change of adapted gains
    pd(1) = -L(1)*roll_d(1)*(rollrate(i) - roll_m(1));
    pd(2) = -L(2)*(rollrate(i) - roll_m(1));
    
    % update the gains
    p(1) = p(1) + pd(1)*dt;
    p(2) = p(2) + pd(2)*dt;
    
    % for plotting only
    ydm(i) = roll_m(1);
    ydes(i) = roll_d;
    phi1(i) = p(1);
    phi2(i) = p(2);

 end
 
 t = 0:dt:Tf-dt;
    
figure(1)
plot(t,rollrate, t, ydm) 
legend('Meas Yaw Rate', 'Model Yaw Rate')
    
figure(2)
plot(t, roll, t, ydes)
legend('Meas Angle', 'Desired Angle')
    
    
figure(3)
plot(t, err)
    
figure(4)
plot(t,phi1, t, phi2)
legend('Phi 1', 'Phi 2')
% 42    24