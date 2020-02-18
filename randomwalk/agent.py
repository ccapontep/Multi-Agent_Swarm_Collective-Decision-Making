# -*- coding: utf-8 -*-
"""
@author: vtrianni and cdimidov
"""
import sys
import random, math, copy
import numpy as np
import string
from pysage import pysage
#from levy_f import stabrnd
from levy_f import distribution_functions
from scipy.stats import wrapcauchy
from scipy.stats import uniform
import scipy

#import numpy.random as R
#import scipyù print word
#from levy_f import MarkovC

class CRWLEVYAgent(pysage.Agent):

    bias = 0;
    linear_speed = 1
    num_motion_steps = 1
    interaction_range = 1


    class Factory:
        def create(self, config_element, arena): return CRWLEVYAgent(config_element, arena)

    ##########################################################################
    # standart init function
    ##########################################################################
    def __init__( self, config_element, arena ):
        pysage.Agent.__init__(self, config_element, arena )

        # parse custom parameters from configuration file

        # control parameter: motion speed
        sspeed = config_element.attrib.get("linear_speed")
        if sspeed is not None:
            CRWLEVYAgent.linear_speed = float(sspeed)

        # control parameter: interaction range
        srange = config_element.attrib.get("interaction_range")
        if srange is not None:
             CRWLEVYAgent.interaction_range = float(srange)

        # control parameter : value of CRW_exponent
        cc= config_element.attrib.get("CRW_exponent")
        if cc is not None:
            CRWLEVYAgent.CRW_exponent = float(cc)
            if (CRWLEVYAgent.CRW_exponent < 0) or (CRWLEVYAgent.CRW_exponent >= 1):
                raise ValueError, "parameter for correlated random walk outside of bounds ( should be in [0,1[ )"

        # control parameter : value of alpha that is the Levy_exponent
        salpha= config_element.attrib.get("levy_exponent")
        if salpha is not None:
            CRWLEVYAgent.levy_exponent = float(salpha)

        # control parameter : value of standard deviation
        ssigma= config_element.attrib.get("std_motion_steps")
        if ssigma is not None:
            CRWLEVYAgent.std_motion_steps = float(ssigma)

        # bias_probability
        sbias_probability = config_element.attrib.get("bias_probability")
        if sbias_probability is not None:
            CRWLEVYAgent.bias_probability= float(sbias_probability)

        # counters for the number of steps used for straight motion
        self.count_motion_steps = 0

        # inventory of target in memory, and list of received target from neighbours
        self.inventory = []
        self.received_targets = []
        self.selected_target = 0

        # counter for the visited targets
        self.visited_target_id = []

        # counter time enter on the target
        self.step_on_target_time = []

        # counter first time enter on target
        self.first_time_step_on_target = []
        self.distance_from_centre=[]

        # flag: true when over target
        self.on_target = False

	# flag: true when over central_place
	self.on_central_place = False


    ##########################################################################
    # String representaion (for debugging)
    ##########################################################################
    def __repr__(self):
        return 'CRWLEVY', pysage.Agent.__repr__(self)


    ##########################################################################
    # equality operator
    ##########################################################################
    def __eq__(self, other):
        if self.inventory_size() != other.inventory_size():
            return False
        return (self.inventory == other.inventory)


    ##########################################################################
    # disequality operator
    ##########################################################################
    def __ne__(self, other):
        if self.inventory_size() != other.inventory_size():
            return True
        return (self.inventory != other.inventory)



    ##########################################################################
    #  initialisation/reset of the experiment variables
    ##########################################################################
    def init_experiment( self ):
        pysage.Agent.init_experiment( self )

        #self.count_motion_steps = stabrnd.stabrnd(CRWLEVYAgent.levy_exponent, 0, CRWLEVYAgent.std_motion_steps, CRWLEVYAgent.average_motion_steps, 1, 1)
        self.count_motion_steps = int(math.fabs(distribution_functions.levy(CRWLEVYAgent.std_motion_steps,CRWLEVYAgent.levy_exponent)))

        # data for passage on target
        self.on_target = False
        self.current_target = None

        # data for colletive decision making
        self.target_committed = None
        self.target_value = 0
        self.target_color = "black"
        self.next_committed_state = None

    ##########################################################################
    # compute the desired motion as a random walk
    ##########################################################################
    def control(self):


        # first check if the agent is passing over any target
        if self.on_target and self.current_target is not None:
            if (self.current_target.position - self.position).get_length() > self.current_target.size:
                self.on_target = False
                self.current_target = None
        else:
            self.on_target = False
            self.current_target = None
            for t in self.arena.targets:
                if (t.position - self.position).get_length() < t.size:
                    self.on_target = True
                    self.current_target = t
                    # self.color = t.color
                    break


        # decision making
        if self.target_committed is None:
            # Discovery
            discovery_value = 0
            discovery_target = None
            discovery_color = "black"
            if self.on_target:
                area_disc = self.current_target.size**2 * math.pi
                area_env = 1
                prob_disc = area_disc / area_env
                # discovery_value  = self.current_target.value * prob_disc * self.arena.timestep_length
                discovery_value  = self.current_target.value * self.arena.timestep_length
                discovery_target = self.current_target.id
                discovery_color  = self.current_target.color

            # Recruitment
            recruitment_value = 0
            recruitment_target = None
            recruitment_color = "black"
            neighbours = self.arena.get_neighbour_agents(self, CRWLEVYAgent.interaction_range)
            if neighbours:
                selected_neighbour = random.choice(neighbours)
                recruitment_value  = selected_neighbour.target_value * self.arena.timestep_length
                recruitment_target = selected_neighbour.target_committed
                recruitment_color  = selected_neighbour.target_color

            if discovery_value + recruitment_value > 1:
                print "[ERROR] Probabilities go over maximimum value"
                sys.exit(2)

            rand_number = random.uniform(0,1)
            if rand_number < discovery_value:
                self.target_committed = discovery_target
                self.target_value     = discovery_value/self.arena.timestep_length
                self.target_color     = discovery_color
                self.arena.update_target_commitment( discovery_target, 1 );
            elif rand_number < discovery_value + recruitment_value:
                self.target_committed = recruitment_target
                self.target_value     = recruitment_value/self.arena.timestep_length
                self.target_color     = recruitment_color
                self.arena.update_target_commitment( recruitment_target, 1 );

        else:
            # Abandonment
            prob_abandonment = 1/ self.target_value * self.arena.timestep_length #0.5; #1.0 - self.current_target.value

            # Cross-Inhibition
            neighbours = self.arena.get_neighbour_agents(self, CRWLEVYAgent.interaction_range)
            prob_crossinhibition = 0
            if neighbours:
                selected_neighbour = random.choice(neighbours)
                if selected_neighbour.target_committed != self.target_committed:
                    # prob_crossinhibition = selected_neighbour.target_value * self.arena.timestep_length #selected_neighbour.target_value
                    prob_crossinhibition = 0.3 * self.arena.timestep_length #selected_neighbour.target_value

            if prob_abandonment + prob_crossinhibition > 1:
                print "[ERROR] Probabilities go over maximimum value"
                sys.exit(2)

            if random.uniform(0,1) < prob_abandonment + prob_crossinhibition:
                self.arena.update_target_commitment( self.target_committed, -1 );
                self.target_committed = None
                self.target_value     = 0
                self.target_color     = "black"




        # agent basic movement: go straight
        self.apply_velocity = pysage.Vec2d(CRWLEVYAgent.linear_speed,0)
        self.apply_velocity.rotate(self.velocity.get_angle())

        # agent random walk: decide step length and turning angle
        self.count_motion_steps -= 1
        if self.count_motion_steps <= 0:
            # step length
            self.count_motion_steps = int(math.fabs(distribution_functions.levy(CRWLEVYAgent.std_motion_steps,CRWLEVYAgent.levy_exponent)))
            # turning angle
            crw_angle = 0
            if CRWLEVYAgent.CRW_exponent == 0:
                crw_angle = random.uniform(0,(2*math.pi))
            else:
                crw_angle = wrapcauchy.rvs(CRWLEVYAgent.CRW_exponent)

            self.apply_velocity.rotate(crw_angle)




pysage.AgentFactory.add_factory("randomwalk.agent", CRWLEVYAgent.Factory())