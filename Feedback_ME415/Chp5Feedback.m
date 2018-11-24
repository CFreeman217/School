A = [-5 -5 4; 2 0 -2; 0 -2 -1];
B = transpose([-2 2 -2]);
C = [1 -3 4];

[P,A_prime] = eig(A);

P
A_prime

inv(P)*A*P