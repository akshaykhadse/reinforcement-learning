# USAGE: python3 process.py inputfile.csv outputfile.csv

import pandas as pd
import numpy as np
import sys

nLines = int(sys.argv[1])+2

csv_data = pd.read_csv(sys.argv[2], header=None).values
mean_measured = np.mean(csv_data, axis=1)
new = mean_measured.reshape(mean_measured.shape[0],-1)

for i in range(nLines):
   with open(sys.argv[3], "a+") as rf:
       rf.write(str(mean_measured[i])+"\n")

