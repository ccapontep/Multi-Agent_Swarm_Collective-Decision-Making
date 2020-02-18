"""
@author: ccapontep
"""
import os, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

directory = os.getcwd()
results_path = os.path.join(directory, "results")
plot_path = os.path.join(results_path, "plots")
# , "QltyValue_" + str(self.targets[0].value) + '_targetDis_' + str(self.targets[0].distance) + '_CRW_' + str(CRWLEVYAgent.CRW_exponent) +  '.txt')

# files_qlty_15 = [idx for idx in os.listdir(results_path) if idx.startswith('QltyValue_1.5')]
# files_qlty_5 = [idx for idx in os.listdir(results_path) if idx.startswith('QltyValue_5.0')]
#all_files = os.listdir(results_path)


all_files = [idx for idx in os.listdir(results_path) if idx.endswith('.txt')]
#all_files = all_files[-1]


for file in all_files:
#    print(all_files)
    file_path = os.path.join(results_path, file)

    with open(file_path, "r") as f:
        RunNum = []
        Time = []
        QtyCommitTarWon = []
        QtyCommitTarLoss = []
        QtyUncommit = []
        times = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

        lines = f.readlines()
        lines = lines[1:]
#        lines = lines[:-1]
        run = []
        run_max_min = []
        
        # check which target wins
        for line in lines:
            values = re.sub('\n', '', line).split('\t')
            run.append(values[0])
            if values[0] == 'final':
                val_max = values.index(str(max(int(values[2]), int(values[3]))))
                val_min = values.index(str(min(int(values[2]), int(values[3]))))
                run_max_min.append(int(run[0]))
                run_max_min.append(val_max)
                run_max_min.append(val_min)
                run = []
        run = []
        # print(lines)
        for line in lines:
            line = re.sub('\n', '', line)
            values = line.split('\t')
            run.append(values[0])
#            print(values)
#            print(run)
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
            
            

        data_df = pd.DataFrame(list(zip(RunNum, Time, QtyCommitTarWon, QtyCommitTarLoss, QtyUncommit)), columns =['Run Number', 'Time', 'Qty Commit Win', 'Qty Commit Loss', 'Qty Uncommit'])
        data_df = data_df.drop(['Run Number'], axis=1)
        data_clean = pd.melt(data_df, id_vars=['Time'])
        data_clean.loc[:,'Time'] /= 60
        data_clean = data_clean[data_clean['Time'].isin(times)]
        
        
#        databytime_df = data_df.set_index(['Time'])
#        time0 = data_df[data_df.Time == 0]
#        time5 = data_df[data_df.Time == 300]
#        time10 = data_df[data_df.Time == 600]
#        time15 = data_df[data_df.Time == 900]
#        time20 = data_df[data_df.Time == 1200]
#        time25 = data_df[data_df.Time == 1500]
        
        fig_dims = (18, 12)
        fig, ax = plt.subplots(figsize=fig_dims)
        plot = sns.boxplot(x="Time", 
                    y="value", 
                    hue="variable", 
                    palette=["blue", "red", "black"], 
                    data=data_clean,
                    ax=ax)

#        plot_fig = plot.get_figure()
        plot_file = file[:-4] + '.png'
#        plot_fig.savefig(plot_file)
        plt.savefig(os.path.join(plot_path, plot_file))
        plt.clf()