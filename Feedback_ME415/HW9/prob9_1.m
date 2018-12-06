G = zpk([], [-1 -1 -10],1);
rlocus(G);
sgrid(0.6, 0);
axis([-14 0 -5 5])

Gc = zpk([-0.1],[0],1);
rlocus(Gc*G);
sgrid(0.6,0);
axis([-14 0 -5 5])

syms t
t = 0:0.0001:60;
G2 = zpk([],[-1 -1 -10],13.6);
G2c = zpk([-0.1], [0 -1 -1 -10],13.4);
step(feedback(G2,1),t);
hold on
step(feedback(G2c,1),t);
grid
xlabel t
ylabel Output
legend('Uncompensated','Compensated')