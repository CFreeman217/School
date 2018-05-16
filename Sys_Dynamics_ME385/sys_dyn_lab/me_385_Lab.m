speed = load('speed.txt');
time = load('time.txt');
t_data = [];
s_data = [];
tau_mult = [];

for i = 1 : length(speed)
    
    if speed(i) > 0
        if length(t_data) == 0
            t_0 = time(i);
        end
        t_data(end+1) = time(i);
        s_data(end+1) = speed(i);
    end
end

w_0 = s_data(end);

for i = 1 : length(t_data)
    if s_data(i) > w_0
        ts_data(i) = w_0;
    else
        ts_data(i) = s_data(i);
    end
    tau_mult(end+1) = -(t_data(i)- t_0)/ log(1-(ts_data(i)/w_0));
end
tau = mean(tau_mult);

fs = 500;
fc = 20;
wn = 2*(fc/fs);
[b,a] = butter(2, wn);
f_data = filter(b,a,s_data);
plot(t_data, f_data);

%plot(t_data, s_data)
