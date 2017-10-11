import glob
import numpy as np
import matplotlib.pyplot as plt
import sys

search_string = sys.argv[1]
search_results = glob.glob(search_string + '*')
# print(search_results)

leg = []
for result in search_results:
    files = glob.glob(result + '/*')
    # print(files)
    result_data = []
    # print(result.split('/')[-1])
    for item in files:
        with open(item, 'r') as resultFile:
            line1 = resultFile.readline()
            line2 = resultFile.readline().rstrip().replace('[', '').replace(']', '').split(', ')
            if len(line2) == 1600:
                result_data.append(line2)
            else:
               print(item)
    result_data = np.array(result_data, dtype=float)
    averaged_results = np.sum(result_data, axis=0) / np.shape(result_data)[0]
    plt.figure(1)
    plt.plot(averaged_results)
    plt.title(result+'/' + 'tuning')
    plt.savefig(result + '/' + result.split('/')[-1] + '.png')
    plt.gcf().clear()
    plt.figure(2)
    plt.plot(averaged_results)
    leg.append(result.split('/')[-1])
plt.legend(leg, loc='lower right')
plt.title(search_string.replace('/', '-') + 'tuning')
plt.savefig(search_string + '/results.png')
print("Use $ [ find . -name '*.png' -type -f -delete ] before running this again")


