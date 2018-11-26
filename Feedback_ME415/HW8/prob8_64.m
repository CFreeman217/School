J1 = 10;
B1 = 1;
k = 100;
Jm = 2;
Bm = 0.5;
os = 5;

p1 = [J1 B1 k];
pm = [Jm Bm k];

Gc = tf([1 0.25],1);
Gp = tf(1, pm)*tf(k,p1);

G = Gc*feedback(Gp, -k);
rlocus(G)
axis([-1 0 -1 1])
z = -log(os/100) / sqrt(pi^2 + log(os/100)^2);
sgrid(z,0);
kd = rlocfind(G);
