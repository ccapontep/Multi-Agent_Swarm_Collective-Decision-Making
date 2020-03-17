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
        self.step_neighbours = []
        self.step_target = None
        self.target_committed = None
        self.target_value = 0
        self.target_color = "black"
        self.next_committed_state = None
        self.decision_made_Neigh = False # save info if decision made by agent

    ##########################################################################
    # compute the desired motion as a random walk
    ##########################################################################
    def control(self, num_steps):

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
                    # check during each time step if the agent is at a target.
                    # If yes, save target information to be used during N step
                    # for decision when agent might not be under a target anymore
                    self.step_target = t
                    break

        # check all neighbors every time step to save their info for later processing
        # in case no neighbors are located at N step when decision is made
        step_neighbours = self.arena.get_neighbour_agents(self, CRWLEVYAgent.interaction_range)
        # if any neighbors available, save to the agent data
        if step_neighbours:
            self.step_neighbours = step_neighbours

        # make a decision every N time steps
        if num_steps % self.arena.decision_step == 0:
            # calculate time scaling from robot to macro
            TimeScaling = round((self.arena.timestep_length * self.arena.time_scale * self.arena.decision_step), 7)

            # decision making
            if self.target_committed is None:
                # Discovery
                discovery_value = 0
                discovery_target = None
                discovery_color = "black"
                if self.on_target or self.step_target:
                    # if there is no current target, but has one target previously
                    # visited then use this as the current target
                    if self.step_target:
                        self.current_target = self.step_target
                    discovery_value  = self.current_target.value * TimeScaling
                    discovery_target = self.current_target.id
                    discovery_color  = self.current_target.color


                # Recruitment
                recruitment_value = 0
                recruitment_target = None
                recruitment_color = "black"
                neighbours = self.arena.get_neighbour_agents(self, CRWLEVYAgent.interaction_range)
                if neighbours or self.step_neighbours:
                    if neighbours:
                        selected_neighbour = random.choice(neighbours)
                    # if neighbor info was saved previously, also recruit
                    elif self.step_neighbours:
                        selected_neighbour = random.choice(self.step_neighbours)
                    recruitment_value  = selected_neighbour.target_value * TimeScaling
                    recruitment_target = selected_neighbour.target_committed
                    recruitment_color  = selected_neighbour.target_color



                if discovery_value + recruitment_value > 1:
                    print "[ERROR] Probabilities go over maximimum value"
                    print repr(discovery_value + recruitment_value)
                    sys.exit(2)


                # self.decision_made_Neigh = False
                # self.decision_made_Targ = False
                rand_number = random.uniform(0,1)
                if rand_number < discovery_value:
                    self.target_committed = discovery_target
                    self.target_value     = discovery_value/TimeScaling
                    self.target_color     = discovery_color
                    self.arena.update_target_commitment( discovery_target, 1 )
                    # self.decision_made_Targ = True

                elif rand_number < discovery_value + recruitment_value:
                    self.target_committed = recruitment_target
                    self.target_value     = recruitment_value/TimeScaling
                    self.target_color     = recruitment_color
                    self.step_neighbours  = None # reset list of neighbors after decision
                    self.arena.update_target_commitment( recruitment_target, 1 );
                #     self.decision_made_Neigh = True
                #
                # else: self.decision_made_Neigh = False

            else:
                # Abandonment
                prob_abandonment = 1/ self.target_value * TimeScaling #0.5; #1.0 - self.current_target.value

                # Cross-Inhibition
                neighbours = self.arena.get_neighbour_agents(self, CRWLEVYAgent.interaction_range)
                prob_crossinhibition = 0
                if neighbours or self.step_neighbours:
                    if neighbours:
                        selected_neighbour = random.choice(neighbours)
                    # if neighbor info was saved previously, also do cross-inhibition
                    elif self.step_neighbours:
                        selected_neighbour = random.choice(self.step_neighbours)

                    if selected_neighbour.target_committed != self.target_committed:
                        prob_crossinhibition = selected_neighbour.target_value * TimeScaling #selected_neighbour.target_value
                        # prob_crossinhibition = 0.3 * TimeScaling #selected_neighbour.target_value


                if prob_abandonment + prob_crossinhibition > 1.0:
                    print "[ERROR] Probabilities go over maximimum value"
                    sys.exit(2)

                # self.decision_made_Neigh = False
                if random.uniform(0,1) < prob_abandonment + prob_crossinhibition:
                    self.arena.update_target_commitment( self.target_committed, -1 );
                    self.target_committed = None
                    self.target_value     = 0
                    self.target_color     = "black"
                    self.step_neighbours  = None # reset list of neighbors when decision made
                    # self.decision_made_Neigh = True

            self.step_target = None # reset info
            self.step_neighbours = None # reset info




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
