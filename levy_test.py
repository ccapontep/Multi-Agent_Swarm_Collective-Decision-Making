# Test the levy std_motion_steps "C"

from levy_f import distribution_functions


std_motion_steps = 100
levy_exponent = 2
qty_run = 100000

results = []
results_t = []

for i in range(qty_run):
    dist = distribution_functions.levy(std_motion_steps, levy_exponent)
    t = dist/std_motion_steps
    results.append(dist)
    results_t.append(t)

avg = sum(results) / float(len(results))
avg_t = sum(results_t) / float(len(results_t))

print(avg, avg_t)
