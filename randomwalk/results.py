"""
@author: vtrianni and cdimidov
"""
import numpy as np
import operator
import scipy.stats as st
import scipy.special as sc

class Results:
    'A class to store the results '

    def __init__( self, config_element ):

        self.num_runs = int(config_element.attrib["num_runs"])

        self.has_converged = []
        self.convergence_time = []
        self.commitment_state = None

        # self.has_converged = np.empty((self.num_runs, 0)).tolist()
        # self.convergence_time = np.empty((self.num_runs, 0)).tolist()
        # self.commitment_state = np.empty((self.num_runs, 0)).tolist()

        self.current_run = -1


    def new_run( self ):
        # self.has_converged.append(False)
        # self.convergence_time.append(0)
        # self.commitment_state.append([])
        self.current_run += 1


    def store( self, has_converged, convergence_time, commitment_state, last_run):
        # self.has_converged[self.current_run] = has_converged
        if last_run == False:
            self.has_converged = self.current_run
            self.convergence_time = convergence_time
            self.commitment_state = commitment_state
        else:
            self.has_converged = 'final'
            self.convergence_time = convergence_time
            self.commitment_state = commitment_state

        # self.has_converged[self.current_run].append(self.current_run)
        # self.convergence_time[self.current_run].append(convergence_time)
        # self.commitment_state[self.current_run].append(commitment_state)

        # print(self.convergence_time)
        # print(np.column_stack((self.has_converged,
        #                         self.convergence_time,
        #                         self.commitment_state)))


    # def save( self, data_filename, run_filename ):
    def save( self, data_filename, save_num ):
        self.save_num = save_num
        all_data = [self.has_converged] + [self.convergence_time] + self.commitment_state
        # for i in range(self.num_runs):
        # has_converged_array = np.matrix(self.has_converged).reshape(len(self.has_converged),1)
        # convergence_time_array = np.matrix(self.convergence_time).reshape(len(self.convergence_time),1)
        # # print(np.matrix(self.commitment_state))
        # commitment_state_array = np.matrix(self.commitment_state).reshape(len(self.commitment_state),3)
        # print(has_converged_array)
        # print(convergence_time_array)
        # print(commitment_state_array.shape)
        # has_converged_array = np.matrix(self.has_converged).reshape(len(self.has_converged),1)
        # convergence_time_array = np.matrix(self.convergence_time).reshape(len(self.convergence_time),1)
        # commitment_state_array = np.matrix(self.commitment_state).reshape(len(self.commitment_state),3)


        # all_data = np.append(has_converged_array, convergence_time_array, axis=0)
        # all_data = np.append(all_data, commitment_state_array, axis=0)

        print(all_data)

        #     print(has_converged_array.shape)
        #     print(convergence_time_array.shape)
        #     print(commitment_state_array.shape)
        #
        #     if i == 0:
        #         has_converged_tot = has_converged_array
        #         convergence_time_tot = convergence_time_array
        #         commitment_state_tot = commitment_state_array
        #     else:
        #         has_converged_tot = np.append(has_converged_tot, has_converged_array, axis=1)
        #         convergence_time_tot = np.append(convergence_time_tot, convergence_time_array, axis=1)
        #         commitment_state_tot = np.append(commitment_state_tot, commitment_state_array, axis=1)
        #
        # all_data = np.append(has_converged_tot, convergence_time_tot, axis=0)
        # all_data = np.append(all_data, commitment_state_tot, axis=0)

        head = 'Run Number  |  Time to Converge  |  Agents Commited to Chosen / Other / Uncommitted Target\n'
        # column_names = np.array('Run Number', 'Time to Converge', 'Agents Commited to Chosen/Other/Uncommitted Target')
        # np.savetxt(data_filename, np.column_stack((has_converged_array,
        #                                            convergence_time_array,
        #                                            commitment_state_array
        #                                          )), fmt="%d %.0f"+" %.0f"*len(self.commitment_state[0]), header=head)
        with open(data_filename, "a+") as f:
            if save_num == 1:
                f.write(head)
                f.write('\t'.join(str(data) for data in all_data))
                f.write('\n')
                    # np.savetxt(f, np.array(all_data), header=head)
            elif save_num == self.num_runs:
                f.write('\t'.join(str(data) for data in all_data))
            else:
                f.write('\t'.join(str(data) for data in all_data))
                f.write('\n')

        # np.savetxt(data_filename, all_data, header=head)
