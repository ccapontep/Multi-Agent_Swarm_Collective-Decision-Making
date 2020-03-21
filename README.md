# Multi-Agent_Swarm_Collective-Decision-Making
Multi-agent simulation environment for mobile agents (kilobots) to test decision making for swarm robots.
See report pdf and ppt presentation for analysis and results.

The goal of the study is understanding the effects of spatiality into a decision-making process in-
spired by the honeybees nest-site selection behaviour. This problem consists in choosing between
two target sites each characterised by a quality value where a higher value describes a better tar-
get. These values provide important information when a decision has to be made by a spatially
dispersed swarm, especially when the targets might need different times to be discovered. The
information about low-quality options should spread slowly, granting time to the robots to possibly
find better-quality options.


An easy and fast decision can be made when the options have different quality values, where the
target with the highest value would win. However, a more complex and interesting scenario is when
both targets have the same quality value, which can lead the swarm to a deadlock situation. In this
case, real bees spread information through the waggle dance and disturb the spread of information
about the competing target using the methods of head-butting and emitting high-pitched beeps, as
mentioned above. Likewise, kilobots and the simulated agents likewise use a decision-making pro-
cess to both simulate the spread of data and the disturbance of such through four decision-making
processes: discovery, recruitment, abandonment and cross-inhibition.

![](results/images/kilobot-simulation.png)
![](results/images/simulation_q5_2mid.png)
![](results/analysis/percent_levy.png)
![](results/analysis/avgtime_distance.png)

Conclusions:

Analyzing all the results of the simulation experiments show that the best performance for both
percentage of converged runs and average time to converge are using ν = 5 and as follows:
• distance = 0.28
• CRW = 0.6 and levy = 2
For avoiding the worst performance, do not use ν = {1.5, 2} and the following parameters:
• distance = 1.06 for percentage of runs converged
• distance = 0.76 for average convergence time
• CRW = 0.9 and levy = 1.2
The lower the quality value, the worse the performance in both percentage of converged runs and
average time to converge.



