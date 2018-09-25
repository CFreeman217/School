import numpy as np, matplotlib.pyplot as plt

fillet_radii = [0.10, 0.25, 0.50, 0.75]

max_stress = [3.302e+4, 2.650e+4, 2.428e+4, 2.301e+4]

plt.plot(fillet_radii, max_stress,marker='.') 
plt.xlabel('Fillet Radius (inches)')
plt.ylabel('Maximum Von Mises Stress (psi)')
plt.title('Stress Concentration Factor and Fillet Radius')
plt.savefig('FEM_003_stressplot.png',bbox_inches = 'tight')
plt.show()