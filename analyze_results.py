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
quorum = 0.7*150

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
#            print(line)
            line = re.sub('\n', '', line)
            values = line.split('\t')
#            print(line)
#            print(values)
            run.append(values[0])
            if values[0] == 'final':
                index_run = int(run[0]) * 3
                RunNum.append(int(run[0]))
                run = []
            else:
#                print(values[0])
                index_run = int(values[0]) * 3
                RunNum.append(int(values[0]))
            Time.append(int(values[1]))
            QtyCommitTarWon.append(int(values[run_max_min[index_run + 1]]))
            QtyCommitTarLoss.append(int(values[run_max_min[index_run + 2]]))
            QtyUncommit.append(int(values[4]))
            
    time = Time[0:16] 
    time_reachedALL = []        
    for i in range(100):
        index_start = i * 16
        index_end = index_start + 16
#        print(index_start, index_end)
        won = QtyCommitTarWon[index_start : index_end]
#        while True:
        if len([*filter(lambda x: x >= quorum, won)]) > 0:
            item_reachedQ = list(filter(lambda j: j >= quorum, won))[0]
            index_reachedQ = won.index(item_reachedQ)
            time_reachedQ = time[index_reachedQ]
            time_reachedALL.append(time_reachedQ)
            
    # write results of each experiment 
    with open(analysis_path, "a+") as f:
        f.write(file.split('.txt')[0] + '\t')
        f.write(str(time_reachedALL) + '\n')

# get data results of all experiments
results = { line.split('\t')[0] : eval(line.split('\t')[1]) for line in open(analysis_path) }

for run_name in results:
    reachedQ = results[run_name]
    reachedPercentage = len(reachedQ) / 100
    if len(reachedQ) > 0:
        reachedTimeAvg = sum(reachedQ) / len(reachedQ) 
        results[run_name].append([reachedPercentage, round(reachedTimeAvg, 2)])
    
    
################################# PLOT ########################################

# plot with increasing distance for % reached quorum and time, CRW and Levy constant
distance_list2 = []
distance_list5 = []
for run_name in results:
    if (run_name.split('_')[1] == '5.0' or run_name.split('_')[1] == '2.0') and run_name.split('_')[5] == '0.0' and run_name.split('_')[7] == '2.0' :
        # for increasing target distance
        output = (results[run_name])[-1]
        output = [float(run_name.split('_')[3])] + output
        if float(run_name.split('_')[1]) == 5.0: distance_list5.append(output)
        else: distance_list2.append(output)
# sort the list to make the target distance in increasing order
distance_list2 = sorted(distance_list2, key=lambda x: x[0])
distance_list5 = sorted(distance_list5, key=lambda x: x[0])
x_distance = [item[0] for item in distance_list2]

y_percentage2 = [int(item[1]*100) for item in distance_list2]
y_avgtime2 = [item[2] for item in distance_list2]

y_percentage5 = [int(item[1]*100) for item in distance_list5]
y_avgtime5 = [item[2] for item in distance_list5]
# create plot for percentage over  distance
plt.xticks(np.arange(0.26, x_distance[-1]+0.1, 0.1))
plt.plot(x_distance, y_percentage2, label = 'quality = 2')
plt.plot(x_distance, y_percentage5, label = 'quality = 5')
plt.xlabel('Distance between Target Options')
plt.ylabel('Percentage of Runs that Converged')
plt.title('Percentage of Convergance with Distance between Target Options')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'percent_distance.png'), dpi=200)
plt.show()

# create plot for avg time over  distance
plt.xticks(np.arange(0.26, x_distance[-1]+0.1, 0.1))
plt.plot(x_distance, y_avgtime2, label = 'quality = 2')
plt.plot(x_distance, y_avgtime5, label = 'quality = 5')
plt.xlabel('Distance between Target Options')
plt.ylabel('Average Time to Converge')
plt.title('Average Time of Convergance with Distance between Target Options')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'avgtime_distance.png'), dpi=200)
plt.show()

# plot with changing CRW keeping Levy parameters and distance constant
levy12 = []
levy16 = []
levy20 = []
for run_name in results:
    if run_name.split('_')[1] == '5.0' and run_name.split('_')[3] == '0.76' :
        # for increasing target distance
        if run_name.split('_')[7] == '1.2':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[5])] + output 
            levy12.append(output)

        elif run_name.split('_')[7] == '1.6':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[5])] + output 
            levy16.append(output)

        elif run_name.split('_')[7] == '2.0':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[5])] + output 
            levy20.append(output)


levy12 = sorted(levy12, key=lambda x: x[0])
levy16 = sorted(levy16, key=lambda x: x[0])
levy20 = sorted(levy20, key=lambda x: x[0])

x_CRW = [item[0] for item in levy12]
y_percentage_l12 = [int(item[1]*100) for item in levy12]
y_avgtime_l12 = [item[2] for item in levy12]

y_percentage_l16 = [int(item[1]*100) for item in levy16]
y_avgtime_l16 = [item[2] for item in levy16]

y_percentage_l20 = [int(item[1]*100) for item in levy20]
y_avgtime_l20 = [item[2] for item in levy20]

# create plot for percentage over  distance
plt.xticks(np.arange(0, x_CRW[-1]+0.3, 0.3))
plt.plot(x_CRW, y_percentage_l12, label = 'levy = 1.2')
plt.plot(x_CRW, y_percentage_l16, label = 'levy = 1.6')
plt.plot(x_CRW, y_percentage_l20, label = 'levy = 2.0')
plt.xlabel('CRW Exponent Parameter')
plt.ylabel('Percentage of Runs that Converged')
plt.title('Percentage of Convergance with CRW Exponent Parameter Increase')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'percent_CRW.png'), dpi=200)
plt.show()

# create plot for avg time over  distance
plt.xticks(np.arange(0, x_CRW[-1]+0.3, 0.3))
plt.plot(x_CRW, y_avgtime_l12, label = 'levy = 1.2')
plt.plot(x_CRW, y_avgtime_l16, label = 'levy = 1.6')
plt.plot(x_CRW, y_avgtime_l20, label = 'levy = 2.0')
plt.xlabel('CRW Exponent Parameter')
plt.ylabel('Avg Time to Converge')
plt.title('Average Time of Convergance with CRW Exponent Parameter Increase')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'avgtime_CRW.png'), dpi=200)
plt.show()



# plot with changing Levy keeping CRW parameters and distance constant
crw0 = []
crw03 = []
crw06 = []
crw09 = []
for run_name in results:
    if run_name.split('_')[1] == '5.0' and run_name.split('_')[3] == '0.76' :
        # for increasing target distance
        if run_name.split('_')[5] == '0.0':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[7])] + output 
            crw0.append(output)

        elif run_name.split('_')[5] == '0.3':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[7])] + output 
            crw03.append(output)

        elif run_name.split('_')[5] == '0.6':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[7])] + output 
            crw06.append(output)
            
        elif run_name.split('_')[5] == '0.9':
            output = (results[run_name])[-1]
#            output = [float(run_name.split('_')[5]), float(run_name.split('_')[7])] + output 
            output = [float(run_name.split('_')[7])] + output 
            crw09.append(output)


crw0 = sorted(crw0, key=lambda x: x[0])
crw03 = sorted(crw03, key=lambda x: x[0])
crw06 = sorted(crw06, key=lambda x: x[0])
crw09 = sorted(crw09, key=lambda x: x[0])

x_Levy = [item[0] for item in crw0]
y_percentage_c0 = [int(item[1]*100) for item in crw0]
y_avgtime_c0 = [item[2] for item in crw0]

y_percentage_c03 = [int(item[1]*100) for item in crw03]
y_avgtime_c03 = [item[2] for item in crw03]

y_percentage_c06 = [int(item[1]*100) for item in crw06]
y_avgtime_c06 = [item[2] for item in crw06]

y_percentage_c09 = [int(item[1]*100) for item in crw09]
y_avgtime_c09 = [item[2] for item in crw09]

# create plot for percentage over  distance
plt.xticks(np.arange(1.2, x_Levy[-1]+0.4, 0.4))
plt.plot(x_Levy, y_percentage_c0, label = 'CRW = 0')
plt.plot(x_Levy, y_percentage_c03, label = 'CRW = 0.3')
plt.plot(x_Levy, y_percentage_c06, label = 'CRW = 0.6')
plt.plot(x_Levy, y_percentage_c09, label = 'CRW = 0.9')
plt.xlabel('Levy Exponent Parameter')
plt.ylabel('Percentage of Runs that Converged')
plt.title('Percentage of Convergance with Levy Parameter Increase')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'percent_levy.png'), dpi=200)
plt.show()

# create plot for avg time over  distance
plt.xticks(np.arange(1.2, x_Levy[-1]+0.4, 0.4))
plt.plot(x_Levy, y_avgtime_c0, label = 'CRW = 0')
plt.plot(x_Levy, y_avgtime_c03, label = 'CRW = 0.3')
plt.plot(x_Levy, y_avgtime_c06, label = 'CRW = 0.6')
plt.plot(x_Levy, y_avgtime_c09, label = 'CRW = 0.9')
plt.xlabel('Levy Exponent Parameter')
plt.ylabel('Avg Time to Converge')
plt.title('Average Time of Convergance with Levy Parameter Increase')
plt.legend()
plt.savefig( os.path.join(results_path, 'analysis', 'avgtime_levy.png'), dpi=200)
plt.show()











    
    
    