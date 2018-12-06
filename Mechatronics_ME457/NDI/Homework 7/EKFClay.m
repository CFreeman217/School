%%% efk %%%
close all
clear all
clc

%data imported
Clay = csvread("NDI_calibration.csv");


t = Clay(:,1);
y = Clay(:,6);
yd = deriv(y,.01);
ca = Clay(:,8);% +1.5;
yy = Clay(:,5);




%% Setting up the model matrices %%
dt = 0.01;
k = 1;
% b = 0.00001; % Damping coefficient
% grav = 9.81; % acceleration due to gravity guess
y(k) = 0; % Guess no acceleration to start
yd(k) = 0; % Guess no velocity  to start
rcu(k) = 0;
rcc(k) = 0;
bias(k) = 0;
N = 9; % number of states

aa(k) = 0;
bb(k) = 0;
cc(k) = 0;
dd(k) =0;
ee(k) = 0;
solve(k) = 0;

% Initial guess for parameters (initial cond. come from first data points)
Xk = [solve(k);aa(k);bb(k);cc(k)]; 

% State update matrix (if nonlinear this may not be a matrix)
% Note: For pendulum, there is sin(angle), therefore not linear

    

 

% Input matrix - No input for pendulum
B = [0;0;0;0;0;0;0];

% Measurement matrix (what do we have estimates of). 
H = [0 1 0 0 0 0 0 0 0 ;
     0 0 0 1 0 0 0 0 0; 
     0 0 0 0 0 0 0 0 1]; % Only measuring angle and velocity



P = eye(N)*.05; % Initial covariance matrix, update number as needed
Q = eye(N)*.0001; 
R = eye(3)*.05; %Size of different measurements (2 measurements here)

for k = 2:length(y)
    
    F = [
    

    %X_pred = A*Xk + B*0 %+ [0; 0; -22.78]; % No Input at the moment
    %X_pred = A*Xk + B*0;% [0; 0; -22.78]; % No Input at the moment
    X_pred(1) = Xk(5)*y(k) + Xk(6)*rcu(k) + Xk(7) +Xk(9)*Xk(8);
    X_pred(2) = Xk(2) ;
    X_pred(3) = Xk(3) ;
    X_pred(4) = Xk(4) ;
    X_pred(5) = Xk(5) ;
    X_pred(6) = Xk(6) ;
    X_pred(7) = Xk(7) ;
    X_pred(8) = Xk(8) ;
    X_pred(9) = Xk(8) ;
    
 
   % X_pred = X_pred;
    
	P_pred = F*P*F' + Q;
    
    
    Z = [y(k);rcu(k);yd(k)]; % New measurements/data
    
    yk = Z - H*X_pred';
    Sk = H*P_pred*H' + R;
    Kk = P_pred*H'*Sk^-1;
    
    
 
    
	Xk = X_pred' + Kk*yk ;
	P = (eye(N) - Kk*H)*P_pred;
    
	y_kal(k) = Xk(1);
	yd_kal(k) = Xk(2);
	ydd_kal(k) = Xk(3);
     
end


yd(1) = 0;
yd(2:k) = diff(y)/dt;
[b,a] = butter(2,20/50);
yd(2:k) = filter(b,a,yd(2:k));


figure(1)
title('Pred')
plot(t, y,'--' ,t, yd_kal)
xlabel('Time [sec]')
ylabel('Pos [m]')
legend('Meas','Kalman')

