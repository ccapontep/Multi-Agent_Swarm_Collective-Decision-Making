# -*- coding: utf-8 -*-
"""
@author: vtrianni and cdimidov
"""
import numpy as np
import math, random
import sys
from pysage import pysage
from results import Results
from agent import CRWLEVYAgent
from target import Target
from collections import defaultdict
import os
directory = os.getcwd()
# Set directory with dataset



class CRWLEVYArena(pysage.Arena): #quindi è una sottoclasse della classe Arena del modulo pysage

    class Factory:
        def create(self, config_element): return CRWLEVYArena(config_element)


    ##########################################################################
    # class init function
    ##########################################################################
    def __init__(self,config_element ):
        pysage.Arena.__init__(self,config_element)


        self.decision_quorum = 1 if config_element.attrib.get("decision_quorum") is None else float(config_element.attrib["decision_quorum"])

        self.timestep_length = 0.5 if config_element.attrib.get("timestep_length") is None else float(config_element.attrib.get("timestep_length"))

        self.time_scale = 0.008 if config_element.attrib.get("time_scale") is None else float(config_element.attrib.get("time_scale"))

        self.size_radius = 0.7506 if config_element.attrib.get("size_radius") is None else float(config_element.attrib.get("size_radius"))


        # is the experiment finished?
        self.has_converged = False
        self.convergence_time = float('nan')
        self.save_num = 0

        self.results_filename   = "CRWLEVY.dat" if config_element.attrib.get("results") is None else config_element.attrib.get("results")
        self.results = Results(config_element)

        # initialise targets from the configuration file
        self.targets = []
        self.num_targets = 0
        for target_element in config_element.iter("target"): # python 2.7
            new_target = Target(target_element)
            self.targets.append(new_target)
            self.num_targets += 1
            print "Initalised target", new_target.id, "(quality value:", new_target.value, ")"


        # initialise num runs from the configuration file
        nnruns = config_element.attrib.get("num_runs")
        if nnruns is not None:
            self.num_runs = int(nnruns)
        else:
            self.num_runs = 1

        #  size_radius
        ssize_radius = config_element.attrib.get("size_radius");
        if ssize_radius is not None:
            self.dimensions_radius = float(ssize_radius)
        elif ssize_radius is None:
            self.dimensions_radius = float(self.dimensions.x/2.0)



    ##########################################################################
    # initialisation of the experiment
    ##########################################################################
    def init_experiment( self ):
        pysage.Arena.init_experiment(self)

        for i in range(self.num_targets):
            target = self.targets[i]
            target.num_committed_agents = 0
            on_target = True

            # Get the location of the first target random and inside circle area environment
            # half the target distance
            while on_target:
                if i == 0:
                    # max_size = (self.dimensions_radius - target.size)
                    max_size = target.distance /2
                    # print max_size
                    while True:
                        x1 = random.uniform(-max_size, max_size)
                        # rand2 = random.uniform(-max_size, max_size)
                        # d1 = math.sqrt((rand1 - 0)**2 + (rand2 - 0)**2)
                        negpos = random.choice((-1, 1))
                        y1 = math.sqrt(max_size**2 - x1**2) * negpos
                        if math.sqrt(x1**2 + y1**2) == max_size:
                            target.position = pysage.Vec2d(x1,y1)
                            print"Target id", i, "is at position", target.position
                            break

            # Get the location of the second target random, but set length away
            # from first target and inside circle area environment
                else:
                    # target.position = pysage.Vec2d(0,0)
                    while True:
                        targetA_pos = self.targets[0].position
                        # angle = random.uniform(0,360)
                        x = targetA_pos[0] * -1
                        y = targetA_pos[1] * -1
                        # x = (target.distance * math.cos(angle)) + targetA_pos[0]
                        # y = (target.distance * math.sin(angle)) + targetA_pos[1]
                        d2 = math.sqrt((x - 0)**2 + (y - 0)**2)
                        if d2 < max_size * 2:
                            target.position = pysage.Vec2d(x,y)
                            print"Target id", i, "is at position", target.position
                            break

                on_target= False
                for j in range(i):
                    t = self.targets[j]
                    if (t.position - target.position).get_length() < (t.size + target.size):
                        on_target = True
                        break


        for agent in self.agents:
            on_target = True
            while on_target:
                max_sizeA = (self.dimensions_radius - agent.size)
                while True:
                    Arand1 = random.uniform(-max_sizeA, max_sizeA)
                    Arand2 = random.uniform(-max_sizeA, max_sizeA)
                    d1 = math.sqrt((Arand1 - 0)**2 + (Arand2 - 0)**2)
                    if d1 < max_sizeA:
                        agent.position = pysage.Vec2d(Arand1,Arand2)
                        # agent.position.rotate(random.uniform(-math.pi,math.pi))
                        break
                # agent.position = pysage.Vec2d(random.uniform(0,max_size),0)
                on_target= False
                for t in self.targets:
                    if (t.position - agent.position).get_length() < t.size:
                        on_target = True
                        break

        self.has_converged = False
        self.convergence_time = float('nan')
        self.results.new_run()

    ##########################################################################
    # run experiment until finished
    def run_experiment( self ):
        results_filename = os.path.join(directory, "results", "QltyValue_" + str(self.targets[0].value) + '_targetDis_' + str(self.targets[0].distance) + '_CRW_' + str(CRWLEVYAgent.CRW_exponent) +  '.txt')

        while not self.experiment_finished():
            minute = self.num_steps/60
            if self.num_steps % (5*60) == 0 : # store values every 5 minutes
                self.save_num += 1
                print'Running for', minute, 'minutes..'
                commitment_state = self.get_commitment_state()
                self.results.store(self.has_converged, self.num_steps, commitment_state, False)
                self.results.save(results_filename, self.save_num)
            self.update()

    ##########################################################################
    # updates the status of the simulation
    ##########################################################################
    def update( self ):
        # computes the desired motion and agent state
        for a in self.agents:
            a.control()
            # if a.step_neighbours: print 'confirmed saved correctly'

        # apply the desired motion
        for a in self.agents:
            a.update()
            if a.position.get_distance((0,0)) > (self.dimensions_radius- a.size):
                current_angle = a.position.get_angle()
                a.position = pysage.Vec2d(self.dimensions_radius- a.size, 0)
                a.position.rotate(current_angle)


        # check convergence
        if self.check_quorum_reached():
            self.has_converged = True
            self.convergence_time = self.num_steps

        # update simulation step counter
        self.num_steps += 1


    ##########################################################################
    # update number of committed agents stored in targets
    #####################################################################
    def update_target_commitment( self, target_id, num_agents):
        for t in self.targets:
            if t.id == target_id:
                t.num_committed_agents += num_agents
                break

    ##########################################################################
    # check quorum reached
    #####################################################################
    def check_quorum_reached( self ):
        max_num_committed = 0
        max_target = None
        for t in self.targets:
            if t.num_committed_agents > max_num_committed:
                max_num_committed = t.num_committed_agents
                max_target = t

        return (float(max_num_committed)/float(self.num_agents) > self.decision_quorum)

    ##########################################################################
    # get committment state
    #####################################################################
    def get_commitment_state(self):
        commitment_state = []
        num_committed = 0
        for t in self.targets:
            commitment_state.append(t.num_committed_agents)
            num_committed += t.num_committed_agents
        commitment_state.append(self.num_agents - num_committed)
        return commitment_state


    ##########################################################################
    # return a list of neighbours
    #####################################################################
    def get_neighbour_agents( self, agent, distance_range ):
        neighbour_list = []
        for a in self.agents:
            if (a is not agent) and ((a.position - agent.position).get_length() < distance_range):
                neighbour_list.append(a)
                # print(neighbour_list)
        return neighbour_list


    ##########################################################################
    # check if the experiment si finished
    ##########################################################################
    def experiment_finished( self ):
        results_filename = os.path.join(directory, "results", "QltyValue_" + str(self.targets[0].value) + '_targetDis_' + str(self.targets[0].distance) + '_CRW_' + str(CRWLEVYAgent.CRW_exponent) +  '.txt')

        conv_time = 0.0
        if ((self.max_steps > 0) and (self.max_steps <= self.num_steps) or self.has_converged):
            conv_time =  self.convergence_time
            print "Run finished: ", self.has_converged, "\tTotal seconds:", self.convergence_time

            commitment_state = self.get_commitment_state()

            self.results.store(self.has_converged, self.convergence_time, commitment_state, True)
            self.results.save(results_filename, self.save_num)
            return True
        return False

    ##########################################################################
    # save results to file, if any
    ##########################################################################
    # def save_results( self ):
    #     self.results.save(self.results_filename,None)

pysage.ArenaFactory.add_factory("randomwalk.arena", CRWLEVYArena.Factory())
