import glob
import numpy as np
import matplotlib.pyplot as plt
import sys

name = sys.argv[1]
results_list = glob.glob(name + '*')

result_data = []
for result in results_list:
    with open(result) as resultFile:
        line1 = resultFile.readline()
        line2 = resultFile.readline().rstrip().replace('[','').replace(']','').split(', ')
        result_data.append(line2)
        line3 = resultFile.readline()
result_data = np.array(result_data, dtype=float)
np.savetxt(name + '.csv', result_data, delimiter=",")
plt.plot(np.sum(result_data, axis=0) / np.shape(result_data)[0])
plt.ylabel('Expected Cumulative Reward')
plt.xlabel('Episode Number')
plt.title(name)
plt.savefig(name + '.png')
plt.close()
