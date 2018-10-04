import os
[os.rename(f, f.replace('.csv', '.txt')) for f in os.listdir('.') if not f.startswith('.')]