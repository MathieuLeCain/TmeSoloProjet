#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 16:09:02 2019

@author: 3700049
"""
GAME_WIDTH = 150
GAME_HEIGHT = 90

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
import math
import sys



class SuperState(SoccerState):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
    
    @property
    def ball(self):
        return self.state.ball.position
    
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
    @property
    def goal_e(self):
        if (self.id_team==1):
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        return Vector2D(0, GAME_HEIGHT/2)
    
    @property
    def goal_a(self):
        if (self.id_team==2):
            return Vector2D(GAME_WIDTH, GAME_HEIGHT/2)
        return Vector2D(0, GAME_HEIGHT/2)
    
    @property
    def dir_ball(self):
#       return (self.state.ball.position - self.state.player_state(self.id_team, self.id_player).position).normalize().scale(5)
        return self.ball - self.player
   
    @property
    def dir_point(self, vec):
        return self.state.position - vec
    
    def distance_balle(self, pointB, distance):
        return (self.state.ball.position.distance(pointB) < distance)
    
    def det_team(nb):
        if(nb == 1):
            return 1
        return 0
    @property
    def dir_ball_acc(self):
        """direction vers balle + acceleration de balle"""
        return ((self.state.ball.vitesse + self.state.ball.position) * 5 - self.state.player_state(self.id_team, self.id_player).position).normalize().scale(5)
    
    @property
    def bait(self):
        if (self.id_team==1):
            return Vector2D(self.player.x, GAME_HEIGHT)
        return Vector2D(self.player.x, 0)
            
    
    def joueur_proche(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if id_player != self.id_player]
        return min([(self.player.distance(player), player) for player in opponents])[1]

    def joueur_proche_a(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player).position for (id_team, id_player) in self.state.players if id_team == self.id_team and id_player != self.id_player]
        return min([(self.player.distance(player), player) for player in opponents])[1]
    
    def passe(self, Vector):
        return Vector.normalize().scale(2.5)
    
    def shoot(self, Vector):
        return Vector.normalize().scale(3.8)
            