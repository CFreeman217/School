num_1 = [1 4 5];
den_1 = [1 9 31 59 60];

tran_1 = tf(num_1, den_1);
% rlocus(tran_1)
num_2 = [1 4];
den_2 = [1 11 18 0];
tran_2 = tf(num_2, den_2);
% rlocus(tran_2)

k = -10;
num_3 = [k];
den_3 = [1 10 35 50 24];
tran_3 = tf(num_3, den_3);
step(tran_3)
% rlocus(tran_3);