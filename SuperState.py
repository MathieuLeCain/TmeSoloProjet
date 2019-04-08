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
       return (self.state.ball.position - self.state.player_state(self.id_team, self.id_player).position).normalize().scale(5)
   
    @property
    def dir_point(self, vec):
        return self.state.position - vec
    
    def distance_balle(self, pointB, distance):
        return (self.state.ball.position.distance(pointB) < distance)
    
    def bait(self):
        if(self.id_team==1):
            return Vector2D(self.player.x, GAME_HEIGHT)
        return Vector2D(self.player.x, 0)
    
    def det_team(nb):
        if(nb == 1):
            return 1
        return 0
    
    def dir_balle_vector(self):
        """direction vers balle + acceleration de balle"""
        dir_balle = self.state.ball.position - self.state.player_state(self.id_team, self.id_player).position
        return (dir_balle.dot(self.ball.next)).normalize.scale(5)
    
    
    def joueur_proche(self, id_team, id_player):
        joueur_actuelle = self.player(id_team, id_player).position
        joueur_proche = self.goal_e
        for i in range(self.nb_players):
            if(i == id_player):
                
            elif(joueur_proche.position.distance(joueur_actuelle) > self.player(id_team, i).position.distance(joueur_actuelle)):
                joueur_proche = self.player(id_team, i).position
        return joueur_proche
    
