# -*- coding: utf-8 -*-
"""
@author: vtrianni and cdimidov
"""

import Tkinter as tk
from pysage import pysage
from agent import CRWLEVYAgent
from target import Target

class CRWLEVYgui(pysage.PysageGUI):

    class Factory:
        def create(self, master, arena, config_element): return CRWLEVYgui(master, arena, config_element)

    def __init__(self, master, arena, config_element):
        self.targets_id = []
        self.central_place = None
        pysage.PysageGUI.__init__(self, master, arena, config_element)

    ##########################################################################
    # GUI intialize function: stup the tk environemt
    def initialize(self):
        pysage.PysageGUI.initialize(self)
        for i in range(self.arena.num_targets):
            t = self.arena.targets[i]
            xpos = int((t.position.x+self.arena.dimensions.x/2.0)*self.pixels_per_meter)
            ypos = int((t.position.y+self.arena.dimensions.y/2.0)*self.pixels_per_meter)
            target_halfsize = int(t.size*self.pixels_per_meter)
            target_tag = "target_%d" % i #allora forse identity non serve visto che c'è già il tag
            self.targets_id.append(self.w.create_oval((xpos-target_halfsize,ypos-target_halfsize,xpos+target_halfsize,ypos+target_halfsize), fill= t.color, stipple='gray50', tags=(target_tag)))
            self.w.tag_bind(target_tag, "<ButtonPress-1>", lambda event, target_tag = target_tag: self.target_selected(event, target_tag))


    def draw_arena(self, init=False):
        self.w.bind("<Button-1>", self.unselect_agent)

        for i in range(self.arena.num_targets):
            t = self.arena.targets[i]
            xpos = int((t.position.x+self.arena.dimensions.x/2.0)*self.pixels_per_meter)
            ypos = int((t.position.y+self.arena.dimensions.y/2.0)*self.pixels_per_meter)
            target_halfsize = int(t.size*self.pixels_per_meter)
            self.w.coords(self.targets_id[i], (xpos-target_halfsize,ypos-target_halfsize,xpos+target_halfsize,ypos+target_halfsize))
            self.w.itemconfig(self.targets_id[i])

        for i in range(self.arena.num_agents):
            a = self.arena.agents[i]
            xpos = int((a.position.x+self.arena.dimensions.x/2.0)*self.pixels_per_meter)
            ypos = int((a.position.y+self.arena.dimensions.y/2.0)*self.pixels_per_meter)
            agent_halfsize = int(pysage.Agent.size*self.pixels_per_meter/2)
            self.w.coords(self.agents_id[i], (xpos-agent_halfsize,ypos-agent_halfsize,xpos+agent_halfsize,ypos+agent_halfsize))
            self.w.itemconfig(self.agents_id[i], fill=a.target_color)









pysage.GUIFactory.add_factory("randomwalk.gui", CRWLEVYgui.Factory())
