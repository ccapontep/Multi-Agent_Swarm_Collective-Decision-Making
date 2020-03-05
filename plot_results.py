"""
@author: Cecilia Aponte
"""
import os, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

directory = os.getcwd()
results_path = os.path.join(directory, "results")
plot_path = os.path.join(results_path, "plots")

# all_files = [idx for idx in os.listdir(results_path) if idx.endswith('QltyValue_4.5_targetDis_0.76_CRW_0.3.txt')]
all_files = [idx for idx in os.listdir(results_path) if idx.endswith('.txt')]
time_incr = 2

for file in all_files:
    file_path = os.path.join(results_path, file)

    with open(file_path, "r") as f:
        RunNum = []
        Time = []
        QtyCommitTarWon = []
        QtyCommitTarLoss = []
        QtyUncommit = []
        times = list(range(0,31, time_incr))[1:]

        lines = f.readlines()
        lines = lines[1:]
        run = []
        run_max_min = []

        # check which target wins
        for line in lines:
            values = re.sub('\n', '', line).split('\t')
            run.append(values[0])
            if values[0] == 'final':
#                print(values)
                val_max = values.index(str(max(int(values[2]), int(values[3]))))
                val_min = values.index(str(min(int(values[2]), int(values[3]))))
#                print('max', val_max, 'min', val_min)
#                print('----------')
                run_max_min.append(int(run[0]))
                run_max_min.append(val_max)
                run_max_min.append(val_min)
                run = []
        run = []
        for line in lines:
            line = re.sub('\n', '', line)
            values = line.split('\t')
            run.append(values[0])
            if values[0] == 'final':
                index_run = int(run[0]) * 3
                RunNum.append(int(run[0]))
                run = []
            else:
                index_run = int(values[0]) * 3
                RunNum.append(int(values[0]))
            Time.append(int(values[1]))
            QtyCommitTarWon.append(int(values[run_max_min[index_run + 1]]))
            QtyCommitTarLoss.append(int(values[run_max_min[index_run + 2]]))
            QtyUncommit.append(int(values[4]))
#            print('won', int(values[run_max_min[index_run + 1]]))
#            print('lost', int(values[run_max_min[index_run + 2]]))
#            print('----------')



        data_df = pd.DataFrame(list(zip(RunNum, Time, QtyCommitTarWon, QtyCommitTarLoss, QtyUncommit)), columns =['Run Number', 'Time', 'Qty Commit Win', 'Qty Commit Loss', 'Qty Uncommit'])
        data_df = data_df.drop(['Run Number'], axis=1)
        data_clean = pd.melt(data_df, id_vars=['Time'])
        data_clean.loc[:,'Time'] /= 60
        data_clean = data_clean[data_clean['Time'].isin(times)]

        fig_dims = (18, 12)
        fig, ax = plt.subplots(figsize=fig_dims)
        plot = sns.boxplot(x="Time",
                    y="value",
                    hue="variable",
                    palette=["blue", "red", "black"],
                    data=data_clean,
                    ax=ax)

        plot_file = file[:-4] + '.png'
        plt.savefig(os.path.join(plot_path, plot_file))
        plt.clf()
