import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob

if sys.argv[1] == '1':
    path = 'report/ex1/'
    filename = glob.glob(path + '*.txt')[0]
    df = pd.read_csv(filename,
                     header=None,
                     sep=' ',
                     names=['s1', 's2', 's3', 's4', 's5', 's6'],
                     dtype=float)

    df.plot()
    plt.yscale('symlog')
    plt.title('Experiment 1')
    plt.xlabel('Number of updates')
    plt.ylabel('Value of each state')
    plt.savefig(path + 'ex1.png')
    # plt.show()

elif sys.argv[1] == '2':
    path = 'report/ex2/'
    filenames = glob.glob(path + '*.txt')
    df = pd.DataFrame()
    for i in range(len(filenames)):
        temp = pd.read_csv(filenames[i], header=None, sep=' ')
        col = filenames[i].replace('.txt', '').replace(path, '')
        df[col] = temp.mean(axis=1)
    df.plot()
    plt.title('Experiment 2')
    plt.xlabel('Number of updates')
    plt.ylabel('Avg value of all states')
    plt.legend(title='Lambda')
    plt.savefig(path + 'ex2.png')
    # plt.show()
