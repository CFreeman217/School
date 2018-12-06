clear all;close all;clc;

% IMPORT DATA HERE -------------------------------------------------------%

%data imported
Clay = csvread("NDI_calibration.csv");


t = Clay(:,1);
y = Clay(:,5); % cmd
%yd = deriv(y,.01); %dcmd
%ca = Clay(:,9);% current angle
yy = Clay(:,6);% current rate

%-------------------------------------------------------------------------%





%FILTER-------------------------------------------------------------------%

[b,a] = butter(2,20/50);


%-------------------------------------------------------------------------%



%-------------------------------------------------------------------------%

n_max = 3;                          % Maximum model order to estimate
u = y;                              % Input data
y_raw = yy;              % Output data
y_rawf = fft(y_raw);
N = length(u);                      % number of data points
time = 1:1:N;

%-------------------------------------------------------------------------%



%MAIN---------------------------------------------------------------------%

% Intializing parameters and bias
params = zeros(n_max+1, n_max);
bias = ones(1,N)';

% Model structure
X = [bias,u,deriv(u,.01),];
Xf = fft(X);

% min order
oo =  size(X,2) -1;

%OLS
n_max = length(X(1,:))-1;
for i = (length(X(1,:))-1):n_max
    params(1:i+1,i) = (Xf'*Xf)\real(Xf'*y_rawf); % Estimated parameters
    % stored in 1:i+1 as it may error out if putting simply : as order
    % of the estimation will increase each loop
    y_est(:,i) = X*params(1:i+1,i);
    SSR(i) = sum((y_est(:,i) - mean(y_raw)).^2);
    SSE(i) = y_raw'*y_raw - params(1:i+1,i)'*X'*y_raw;
    %X = [X, u.^(i+1)];% update regressor matrix for next iteration
end

figure
plot(time,y_raw,time,y_est(:,n_max))
xlabel('Time')
ylabel('output')
legend('measured','Freq OLS')

figure
res =  y_raw -y_est(:,oo);
plot(time,res,'.')
xlabel('Time')
ylabel('Res')

% resudu vs output
figure
plot(y_est(:,oo),res,'.')
xlabel('output')
ylabel('res')


% Plotting the 4 different models.
figure
plot(time,y_raw,'black',time,y_est(:,oo))%,time,y_est(:,3))%,time,y_est(:,4))
legend('Measured','Model')
xlabel('Time')
ylabel('Output')
