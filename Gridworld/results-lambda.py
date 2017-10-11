import glob
import numpy as np
import matplotlib.pyplot as plt
import sys

search_string = sys.argv[1]
search_results = glob.glob(search_string + '*')
# print(search_results)

avg = {}
for result in search_results:
    files = glob.glob(result + '/*')
    # print(files)
    result_data = []
    # print(result.split('/')[-1])
    for item in files:
        with open(item, 'r') as resultFile:
            line1 = resultFile.readline()
            line2 = resultFile.readline().rstrip().replace('[', '').replace(']', '').split(', ')
            if len(line2) == 500:
                result_data.append(line2)
            else:
               print(item)
    result_data = np.array(result_data, dtype=float)
    avg[result.split('/')[-1]] = np.mean(result_data)
    
    with open(result + '/' + result.split('/')[-1] + '.md', 'w') as outFile:
        outFile.write(str(avg.keys()))
        outFile.write('\n')
        outFile.write(str(avg.values()))

x = []
y = []
for key in sorted(avg.keys()):
    x.append(key)
    y.append(avg[key])    
plt.figure(2)   
plt.plot(x, y)
plt.xlabel('lambda')
plt.ylabel('Expected cumulative reward over 500 episodes')  
plt.title(search_string.replace('/', '-') + 'tuning')
plt.savefig(search_string + '/results.png')
print("Use $ [ find . -name '*.png' -type -f -delete ] before running this again")


