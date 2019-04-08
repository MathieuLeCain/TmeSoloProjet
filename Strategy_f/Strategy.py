#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:23:34 2019

@author: 3771920
"""

GAME_WIDTH = 150
GAME_HEIGHT = 90
PLAYER_RADIUS = 1.
BALL_RADIUS = 0.65
CAN_SHOOT = PLAYER_RADIUS + BALL_RADIUS
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from tools import SuperState

class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Echauffement")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if(self.engage==0):
            self.engage=1
            return SoccerAction(Vector2D(0,0), s.player_e - s.player)
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(s.dir_ball.norm < CAN_SHOOT):
            return SoccerAction(s.dir_ball.scale(5.0), s.player_e - s.player)
        return SoccerAction(s.dir_ball.scale(5.0), (Vector2D(0,0)))

class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if(self.engage==0):
            self.engage=1
            return SoccerAction(Vector2D(0,0), s.player_e - s.player)
        
        if (s.ball.x > GAME_WIDTH/2 and id_team==0):
            return(Vector2D(GAME_WIDTH/4, GAME_HEIGHT/2) - s.player)
        elif (s.ball.x < GAME_WIDTH/2 and id_team==1):
            return(Vector2D(GAME_WIDTH*3/4, GAME_HEIGHT/2) - s.player)
            
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(s.dir_ball.norm < CAN_SHOOT):
            return SoccerAction(s.dir_ball.scale(5.0), s.player_e - s.player)
        return SoccerAction(s.dir_ball.scale(5.0), (Vector2D(0,0)))
    
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Player 1", Echauffement())  # Random strategy
team2.add("Player 2", Echauffement())   # Random strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)