"""
@author: Cecilia Aponte
"""
import numpy as np
import operator
import scipy.stats as st
import scipy.special as sc

class Results:
    'A class to store the results '

    def __init__( self, config_element ):

        self.num_runs = int(config_element.attrib["num_runs"])
        self.steps_run = int(config_element.attrib["steps_run"])

        self.has_converged = []
        self.convergence_time = []
        self.commitment_state = None

        self.current_run = -1
        self.start = True


    def new_run( self ):
        self.current_run += 1



    def store( self, has_converged, convergence_time, commitment_state, last_run):
        if last_run == False:
            self.has_converged = self.current_run
            self.convergence_time = convergence_time
            self.commitment_state = commitment_state
        else:
            self.has_converged = 'final'
            self.convergence_time = convergence_time
            self.commitment_state = commitment_state

    def save( self, data_filename, save_num ):
        self.save_num = save_num
        if self.save_num == 2: self.start = False # to place header in saved txt

        all_data = [self.has_converged] + [self.convergence_time] + self.commitment_state

        print(all_data)

        head = 'Run Number  |  Time to Converge  |  Agents Commited to Chosen / Other / Uncommitted Target\n'
        with open(data_filename, "a+") as f:
            if self.start == True:
                f.write(head)
                f.write('\t'.join(str(data) for data in all_data))
                f.write('\n')
            elif save_num != self.steps_run and save_num != 1:
                f.write('\t'.join(str(data) for data in all_data))
                f.write('\n')
            else:
                f.write('\t'.join(str(data) for data in all_data))
                f.write('\n')
