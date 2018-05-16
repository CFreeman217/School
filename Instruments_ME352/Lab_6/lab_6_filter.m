fs = 15000; % Sampling Frequency
fc = 20; % Cutoff Frequency
Wn = 2*fc/fs; % Natural Frequency
[b,a] = butter(2, Wn); % Butterworth parameters - 2nd order
f_data = filter(b,a, data);  % Filtering
d_force = plot(f_data(:,1), f_data(:,3));
graphDialog('Click two points on the graph to find mean.');
[x,y] = ginput(2);
fprintf('Data Point : % \t Value : %',f_data(x(1):1), f_data(x(1):3));

E = abs((y(1)-y(2))/(x(1)-x(2)));
