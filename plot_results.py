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
analysis_path = os.path.join(results_path, 'analysis', "analysis.txt")


# all_files = [idx for idx in os.listdir(results_path) if idx.endswith('QltyValue_4.5_targetDis_0.76_CRW_0.3.txt')]
all_files = [idx for idx in os.listdir(results_path) if idx.endswith('.txt')]
time_incr = 2
item = 0

for file in all_files:
    file_path = os.path.join(results_path, file)
    item += 1

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
#            print(line)
#            print(file)
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
#        fig, ax = plt.subplots(figsize=fig_dims)
#        plot = sns.boxplot(x="Time",
#                    y="value",
#                    hue="variable",
#                    palette=["blue", "red", "black"],
#                    data=data_clean,
#                    ax=ax)

#        plot_file = file[:-4] + '.png'
#        plt.savefig(os.path.join(plot_path, plot_file))
#        plt.clf()

        
        
        
#medians = data_clean.groupby(['Time', "variable"])['value'].median()
#q25 = data_clean.groupby(['Time', "variable"])['value'].quantile(0.25)
#q75 = data_clean.groupby(['Time', "variable"])['value'].quantile(0.75)
        
        # get median and interquartile range (at 25% and 75%)
#        if float(file[:-4].split('_')[5]) == 0.0 and float(file[:-4].split('_')[7]) == 2.0 and (float(file[:-4].split('_')[1]) == 5.0 or float(file[:-4].split('_')[1]) == 1.5):
        
        # Get the dataframes when levy = 1.2 and q=5 and distance=0.76
        if float(file[:-4].split('_')[3]) == 0.76 and float(file[:-4].split('_')[7]) == 1.2 and float(file[:-4].split('_')[1]) == 5.0:
            if float(file[:-4].split('_')[5]) == 0.0:
                data_CRW00_levy12 = pd.melt(data_df, id_vars=['Time'])
                data_CRW00_levy12.loc[:,'Time'] /= 60
#                data_CRW00_levy12['CRW'] = 0.0
                data_CRW00_levy12 = data_CRW00_levy12[data_CRW00_levy12['Time'].isin(times)]
                data_CRW00_levy12['variable'] = 'CRW=0.0_' + data_CRW00_levy12['variable'].astype(str)

            elif float(file[:-4].split('_')[5]) == 0.3:
                data_CRW03_levy12 = pd.melt(data_df, id_vars=['Time'])
                data_CRW03_levy12.loc[:,'Time'] /= 60
#                data_CRW03_levy12['CRW'] = 0.3
                data_CRW03_levy12 = data_CRW03_levy12[data_CRW03_levy12['Time'].isin(times)]
                data_CRW03_levy12['variable'] = 'CRW=0.3_' + data_CRW03_levy12['variable'].astype(str)

            elif float(file[:-4].split('_')[5]) == 0.6:
                data_CRW06_levy12 = pd.melt(data_df, id_vars=['Time'])
                data_CRW06_levy12.loc[:,'Time'] /= 60
#                data_CRW06_levy12['CRW'] = 0.6
                data_CRW06_levy12 = data_CRW06_levy12[data_CRW06_levy12['Time'].isin(times)]
                data_CRW06_levy12['variable'] = 'CRW=0.6_' + data_CRW06_levy12['variable'].astype(str)

            elif float(file[:-4].split('_')[5]) == 0.9:
                data_CRW09_levy12 = data_clean.copy()
                data_CRW09_levy12 = pd.melt(data_df, id_vars=['Time'])
#                data_CRW09_levy12['CRW'] = 0.9
                data_CRW09_levy12.loc[:,'Time'] /= 60
                data_CRW09_levy12 = data_CRW09_levy12[data_CRW09_levy12['Time'].isin(times)]
                data_CRW09_levy12['variable'] = 'CRW=0.9_' + data_CRW09_levy12['variable'].astype(str)

                
            
        # Get the dataframes when levy = 1.6 and q=5 and distance=0.76
        if float(file[:-4].split('_')[3]) == 0.76 and float(file[:-4].split('_')[7]) == 1.6 and float(file[:-4].split('_')[1]) == 5.0:
            if float(file[:-4].split('_')[5]) == 0.0:
                data_CRW00_levy16 = pd.melt(data_df, id_vars=['Time'])
                data_CRW00_levy16.loc[:,'Time'] /= 60
                data_CRW00_levy16 = data_CRW00_levy16[data_CRW00_levy16['Time'].isin(times)]
                data_CRW00_levy16['variable'] = 'CRW=0.0_' + data_CRW00_levy16['variable'].astype(str)
            elif float(file[:-4].split('_')[5]) == 0.3:
                data_CRW03_levy16 = pd.melt(data_df, id_vars=['Time'])
                data_CRW03_levy16.loc[:,'Time'] /= 60
                data_CRW03_levy16 = data_CRW03_levy16[data_CRW03_levy16['Time'].isin(times)]
                data_CRW03_levy16['variable'] = 'CRW=0.3_' + data_CRW03_levy16['variable'].astype(str)
                
            elif float(file[:-4].split('_')[5]) == 0.6:
                data_CRW06_levy16 = pd.melt(data_df, id_vars=['Time'])
                data_CRW06_levy16.loc[:,'Time'] /= 60
                data_CRW06_levy16 = data_CRW06_levy16[data_CRW06_levy16['Time'].isin(times)]
                data_CRW06_levy16['variable'] = 'CRW=0.6_' + data_CRW06_levy16['variable'].astype(str)
                
            elif float(file[:-4].split('_')[5]) == 0.9:
                data_CRW09_levy16 = pd.melt(data_df, id_vars=['Time'])
                data_CRW09_levy16.loc[:,'Time'] /= 60
                data_CRW09_levy16 = data_CRW09_levy16[data_CRW09_levy16['Time'].isin(times)]
                data_CRW09_levy16['variable'] = 'CRW=0.9_' + data_CRW09_levy16['variable'].astype(str)
                
        # Get the dataframes when levy = 2.0 and q=5 and distance=0.76
        if float(file[:-4].split('_')[3]) == 0.76 and float(file[:-4].split('_')[7]) == 2.0 and float(file[:-4].split('_')[1]) == 5.0:
            if float(file[:-4].split('_')[5]) == 0.0:
                data_CRW00_levy10 = pd.melt(data_df, id_vars=['Time'])
                data_CRW00_levy10.loc[:,'Time'] /= 60
                data_CRW00_levy10 = data_CRW00_levy10[data_CRW00_levy10['Time'].isin(times)]
                data_CRW00_levy10['variable'] = 'CRW=0.0_' + data_CRW00_levy10['variable'].astype(str)
            elif float(file[:-4].split('_')[5]) == 0.3:
                data_CRW03_levy20 = pd.melt(data_df, id_vars=['Time'])
                data_CRW03_levy20.loc[:,'Time'] /= 60
                data_CRW03_levy20 = data_CRW03_levy20[data_CRW03_levy20['Time'].isin(times)]
                data_CRW03_levy20['variable'] = 'CRW=0.3_' + data_CRW03_levy20['variable'].astype(str)
                
            elif float(file[:-4].split('_')[5]) == 0.6:
                data_CRW06_levy20 = pd.melt(data_df, id_vars=['Time'])
                data_CRW06_levy20.loc[:,'Time'] /= 60
                data_CRW06_levy20 = data_CRW06_levy20[data_CRW06_levy20['Time'].isin(times)]
                data_CRW06_levy20['variable'] = 'CRW=0.6_' + data_CRW06_levy20['variable'].astype(str)
                
            elif float(file[:-4].split('_')[5]) == 0.9:
                data_CRW09_levy20 = pd.melt(data_df, id_vars=['Time'])
                data_CRW09_levy20.loc[:,'Time'] /= 60
                data_CRW09_levy20 = data_CRW09_levy20[data_CRW09_levy20['Time'].isin(times)]
                data_CRW09_levy20['variable'] = 'CRW=0.9_' + data_CRW09_levy20['variable'].astype(str)
                
result_levy12 = pd.concat([data_CRW00_levy12, data_CRW03_levy12, data_CRW06_levy12, data_CRW09_levy12], ignore_index=True)
result_levy16 = pd.concat([data_CRW00_levy16, data_CRW03_levy16, data_CRW06_levy16, data_CRW09_levy16], ignore_index=True)
result_levy20 = pd.concat([data_CRW00_levy20, data_CRW03_levy20, data_CRW06_levy20, data_CRW09_levy20], ignore_index=True)

                    
#dataframes = [ CRW00_levy12, CRW03_levy12, CRW06_levy12, CRW09_levy12 ]
colors = [['blue', 'red', 'black'], ['skyblue', 'salmon', 'lightgray'], ['midnightblue', 'firebrick', 'dimgrey'], ['darkorange', 'teal', 'brown']]
fig, ax = plt.subplots(figsize=fig_dims)
#palette=["blue", "red", "black"]
CRW_color = ['blue', 'red', 'black', 'green']
colors_all = ['blue', 'red', 'black', 'skyblue', 'salmon', 'lightgray', 'midnightblue', 'firebrick', 'dimgrey', 'darkorange', 'teal', 'brown']

result_levy12_win = result_levy12[~result_levy12['variable'].str.endswith('Qty Commit Loss')]
result_levy12_win = result_levy12_win[~result_levy12_win['variable'].str.endswith('Qty Uncommit')]

result_levy12_loss = result_levy12[~result_levy12['variable'].str.endswith('Qty Commit Win')]
result_levy12_loss = result_levy12_loss[~result_levy12_loss['variable'].str.endswith('Qty Uncommit')]


#for n in range(4):
ax = sns.boxplot( data= result_levy12_win, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy12_win.png'))
plt.clf()
#plt.show()
fig1, ax1 = plt.subplots(figsize=fig_dims)
ax1 = sns.boxplot( data= result_levy12_loss, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax1)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy12_loss.png'))
#plt.show()
plt.clf()


result_levy16_win = result_levy16[~result_levy16['variable'].str.endswith('Qty Commit Loss')]
result_levy16_win = result_levy16_win[~result_levy16_win['variable'].str.endswith('Qty Uncommit')]

result_levy16_loss = result_levy16[~result_levy16['variable'].str.endswith('Qty Commit Win')]
result_levy16_loss = result_levy16_loss[~result_levy16_loss['variable'].str.endswith('Qty Uncommit')]

fig, ax = plt.subplots(figsize=fig_dims)
ax = sns.boxplot( data= result_levy16_win, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy16_win.png'))
plt.clf()
#plt.show()
fig1, ax1 = plt.subplots(figsize=fig_dims)
ax1 = sns.boxplot( data= result_levy16_loss, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax1)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy16_loss.png'))
#plt.show()
plt.clf()


result_levy20_win = result_levy20[~result_levy20['variable'].str.endswith('Qty Commit Loss')]
result_levy20_win = result_levy20_win[~result_levy20_win['variable'].str.endswith('Qty Uncommit')]

result_levy20_loss = result_levy20[~result_levy20['variable'].str.endswith('Qty Commit Win')]
result_levy20_loss = result_levy20_loss[~result_levy20_loss['variable'].str.endswith('Qty Uncommit')]

fig, ax = plt.subplots(figsize=fig_dims)
ax = sns.boxplot( data= result_levy20_win, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy20_win.png'))
plt.clf()
#plt.show()
fig1, ax1 = plt.subplots(figsize=fig_dims)
ax1 = sns.boxplot( data= result_levy20_loss, x='Time', y='value', palette = CRW_color, hue='variable', ax=ax1)
plt.savefig(os.path.join(results_path, 'analysis', 'compareCRW_levy20_loss.png'))
#plt.show()
plt.clf()
            

    
#            def q1(x):
#                return x.quantile(0.25)
#            
#            def q2(x):
#                return x.quantile(0.75)
#            
#            f = {'median', q1,q2}
#            avg_quartile = data_clean.groupby(['Time', "variable"])['value'].agg(f)
#            avg_quartile['QltyValue'] = float(file[:-4].split('_')[1])
#    #        avg_quartile['Time'] = avg_quartile.index.get_level_values('Time')
#    #        avg_quartile['variable'] = avg_quartile.index.get_level_values('variable')
#            
#            # merge all dataframes 
#            if item == 1:
#                result = avg_quartile.copy()
#            else:
##                result = pd.merge(result, avg_quartile, on=['Time', 'variable'])
#                result = result.append(avg_quartile, ignore_index=False)
#            del avg_quartile   

