import pandas as pd
import matplotlib.pyplot as plt

# auxilary file
# used to split up timing data by pid


def main():
    df = pd.read_csv('out.csv', sep = ',')

    pids = df.pid.unique()

    p0 = df[df.pid == pids[0]]
    p1 = df[df.pid == pids[1]]
    p2 = df[df.pid == pids[2]]
    p3 = df[df.pid == pids[3]]
    p4 = df[df.pid == pids[4]]

    p0.to_csv('p0.csv')
    p1.to_csv('p1.csv')
    p2.to_csv('p2.csv')
    p3.to_csv('p3.csv')
    p4.to_csv('p4.csv')

    #plt.scatter(p0.loc[:,'time'], p0.loc[:,'size'])
    #plt.show()

if __name__ == '__main__':
    main()