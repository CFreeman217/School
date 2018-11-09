'''
System checker to make sure all the nessecary libraries are installed on the machine.
'''
import sys
print('Python: {}'.format(sys.version))
# Scipy
import scipy
print('SciPy: {}'.format(scipy.__version__))
# Numpy
import numpy
print('NumPy: {}'.format(numpy.__version__))
# MatPlotLib
import matplotlib
print('matplotlib: {}'.format(matplotlib.__version__))
# Pandas
import pandas
print('pandas: {}'.format(pandas.__version__))
# scikit-learn
import sklearn
print('sklearn: {}'.format(sklearn.__version__))
print('Success! This computer has all of the modules needed to do computer learning')