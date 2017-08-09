import pandas as pd
import numpy as np

csv_file = "output.csv"
result_csv = "result.csv"

csv_data = pd.read_csv(csv_file, header=None).values
mean_measured = np.mean(csv_data, axis=1)
new = mean_measured.reshape(mean_measured.shape[0],-1)

for i in range(1001):
   with open(result_csv, "a+") as rf:
       rf.write(str(mean_measured[i])+"\n")

