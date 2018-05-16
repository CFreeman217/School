import os
[os.rename(f, f.replace('displacement', 'displacement_2')) for f in os.listdir('.')]