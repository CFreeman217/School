% numg = [1 4 5];
numg = 11 * [1 4 5];
deng = conv([1 2 5], poly([-3 -4]));
G = tf(numg,deng);
T = feedback(G,1);
% rlocus(G)
% axis equal
step(T)