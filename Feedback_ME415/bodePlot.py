from scipy import signal
import matplotlib.pyplot as plt

numg = [50]
deng = [1, 9, 18, 0]

tf = signal.TransferFunction(numg, deng)

w, mag, phase = signal.bode(tf)
fig, ax = plt.subplots(2, sharex=True)
ax[0].semilogx(w, mag)
ax[0].set_title('Bode Plot\nMagnitude')
ax[0].grid(True, which='both')
ax[1].semilogx(w, phase)
ax[1].set_title('Phase Angle')
ax[1].grid(True, which='both')
plt.show()