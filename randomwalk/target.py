"""
@author: vtrianni and cdimidov
"""
import random, math, copy
import numpy as np
from pysage import pysage


########################################################################################
## Pysage Target
########################################################################################

##########################################################################
# the main target class
class Target:
    'Definition of a target in 2D space'

    ##########################################################################
    # standard initialisation
    def __init__(self, target_id, size, value, color, distance):
        # identification target
        self.id = target_id

        # position in meters
        self.position = pysage.Vec2d(0,0)

        # value of the target (aggiunto da Violetta)
        self.value = value

        # size of the target (radius)
        self.size = size

        # color of the target
        self.color = color

        # number of agents commited to this target
        self.num_committed_agents = 0

        # number of targets initialized
        self.targets_init = 0

        # distance between targets
#        self.distance = distance

    ##########################################################################
    # XML initialisation
    def __init__(self, config_element):
        # identification target
        self.id = config_element.attrib.get("id")
        if self.id is None:
            print "[ERROR] missing attribute 'id' in tag <subnet>"
            sys.exit(2)


#        if self.id == 'B':
#            print("target id", self.id, "is distance away", positionA)

        # position in meters
        self.position = pysage.Vec2d(0,0)

        # value of the target (aggiunto da Violetta)
        self.value = 1 if config_element.attrib.get("value") is None else float(config_element.attrib["value"])

        # size of the target (radius)
        self.size = 0.02 if config_element.attrib.get("size") is None else float(config_element.attrib["size"])

        # color of the target
        self.color = "black" if config_element.attrib.get("color") is None else config_element.attrib["color"]

        # number of agents commited to this target
        self.num_committed_agents = 0

        # distance between targets
        self.distance = 0.7 if config_element.attrib.get("distance") is None else float(config_element.attrib["distance"])

    ##########################################################################
    # String representaion (for debugging)
    def __repr__(self):
        return 'Target %d(%s, %s)' % ( self.id, self.position.x, self.position.y)
