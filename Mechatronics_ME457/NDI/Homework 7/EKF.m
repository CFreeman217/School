%%% Kalman Filter with Pendulum Data (no input) %%%
close all
clear all
clc

%data imported
load msd_data_hw7-1;

t = msd.t;
y = msd.y;
ydd = msd.ydd;
g= -9.81;



%% Setting up the model matrices %%
dt = 0.01;
k = 1;
% b = 0.00001; % Damping coefficient
% grav = 9.81; % acceleration due to gravity guess
ydd(k) = 0; % Guess no acceleration to start
yd(k) = 0; % Guess no velocity  to start

N = 6; % number of states

aa(k) = 0;
bb(k) = -6;
cc(k) = -12;

% Initial guess for parameters (initial cond. come from first data points)
Xk = [y(k); yd(k); ydd(k); aa(k); bb(k); cc(k)]; 

% State update matrix (if nonlinear this may not be a matrix)
% Note: For pendulum, there is sin(angle), therefore not linear
F = [1 dt dt^2/2 0 0 0;
     0 1 dt 0 0 0;
     aa(k) bb(k) 0 0 0 cc(k);
     0 0 0 1 0 0;
     0 0 0 0 1 0;
     0 0 0 0 0 1];

 

% Input matrix - No input for pendulum
B = [0 0; 0 0; 0 0];

% Measurement matrix (what do we have estimates of). 
H = [1 0 0 0 0 0;
     0 0 1 0 0 0]; % Only measuring angle and velocity



P = eye(N)*.05; % Initial covariance matrix, update number as needed
Q = eye(N)*.005; 
R = eye(2)*.1; %Size of different measurements (2 measurements here)

for k = 2:length(y)
    %X_pred = A*Xk + B*0 %+ [0; 0; -22.78]; % No Input at the moment
    %X_pred = A*Xk + B*0;% [0; 0; -22.78]; % No Input at the moment
    X_pred(1) = Xk(1) + Xk(2)*dt + Xk(3)*dt^2/2;
    X_pred(2) = Xk(2) + Xk(3)*dt;
    X_pred(3) = Xk(4)*Xk(1) + Xk(5)*Xk(2) + Xk(6);
    X_pred(4) = Xk(4);
    X_pred(5) = Xk(5);
    X_pred(6) = Xk(6);
    X_pred = X_pred;
    
	P_pred = F*P*F' + Q;
    
    
    Z = [y(k); ydd(k)]; % New measurements/data
    
    yk = Z - H*X_pred';
    Sk = H*P_pred*H' + R;
    Kk = P_pred*H'*Sk^-1;
    
%     Xk(1) = X_pred(1) + Kk*yk;
%     Xk(2) = X_pred(2) + Kk*yk;
%     Xk(3) = X_pred(3) + Kk*yk;
%     Xk(4) = X_pred(4) + Kk*yk;
%     Xk(5) = X_pred(5) + Kk*yk;
%     Xk(6) = X_pred(6) + Kk*yk;
    
	Xk = X_pred + Kk*yk;
	P = (eye(N) - Kk*H)*P_pred;
    
	y_kal(k) = Xk(1);
	yd_kal(k) = Xk(2);
	ydd_kal(k) = Xk(3);
    gamma(k) = Xk(4);
    gamma2(k) = Xk(5);
    gamma3(k) = Xk(6);
     
end

yd(1) = 0;
yd(2:k) = diff(y)/dt;
[b,a] = butter(2,20/50);
yd(2:k) = filter(b,a,yd(2:k));

figure(1)

subplot(3,1,1);
title('Postition')
plot(t, y_kal)
xlabel('Time [sec]')
ylabel('Pos [m]')
legend('Kalman')

subplot(3,1,2);
title('Velocity')
plot(t, yd_kal)
xlabel('Time [sec]')
ylabel('Velocity [m/s]')
legend('Kalman')

subplot(3,1,3);
title('Accleration')
plot(t,ydd_kal)
xlabel('Time [sec]')
ylabel('Acceleration [m/s^2]')
legend('Kalman')

figure(2)

subplot(3,1,1);
title('PostitionCo')
plot(t, gamma)
xlabel('Time [sec]')
ylabel('')
legend('Pco')

subplot(3,1,2);
title('VelocityCo')
plot(t, gamma2)
xlabel('Time [sec]')
ylabel('')
legend('Vco')

subplot(3,1,3);
title('AcclerationCo')
plot(t,gamma3)
xlabel('Time [sec]')
ylabel('')
legend('Aco')


