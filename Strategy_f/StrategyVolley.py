#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:23:34 2019

@author: 3771920
"""

GAME_WIDTH = 180
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
            return SoccerAction(Vector2D(0,0), (s.player_e - s.player).normalize().scale(3.0))
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(s.dir_ball.norm < CAN_SHOOT):
            return SoccerAction(s.dir_ball.normalize().scale(5.0), (s.player_e - s.player).normalize().scale(3.0))
        return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(0,0)))

class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(self.engage==0):
            self.engage=1
            return SoccerAction(Vector2D(0,0), s.player_e - s.player)

            
        if(s.dir_ball.norm < CAN_SHOOT):
            if(id_team==1):
                return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(GAME_WIDTH, GAME_HEIGHT-10) - s.player).normalize().scale(3.8))     
            return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(0, GAME_HEIGHT - s.player_e.y) - s.player).normalize().scale(3.8))
            
            if(abs(GAME_HEIGHT/2 - s.player_e.y) < 10):
                return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(0, 10) - s.player).normalize().scale(3.8))       
            return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(GAME_WIDTH, GAME_HEIGHT - s.player_e.y) - s.player).normalize().scale(3.8))
        return SoccerAction(s.dir_ball.normalize().scale(5.0), (Vector2D(0,0)))
    
class Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defense")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(self.engage==0):
            self.engage=1
            return SoccerAction(Vector2D(0,0), s.player_e - s.player)

        if (s.ball.x > GAME_WIDTH/2 and id_team==1):
            direction = Vector2D(GAME_WIDTH/3 - s.player.x , GAME_HEIGHT/2- s.player.y).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))
        elif (s.ball.x < GAME_WIDTH/2 and id_team==2):
            direction = (Vector2D((GAME_WIDTH)*2/3, GAME_HEIGHT/2) - s.player).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))

            
        if(s.dir_ball.norm < CAN_SHOOT):
            if(id_team==1):
                return SoccerAction(s.dir_ball.normalize().scale(5.0), Vector2D(GAME_WIDTH, GAME_HEIGHT) - s.player)    
            return SoccerAction(s.dir_ball, Vector2D(0,0) - s.player)

        return SoccerAction(s.dir_ball, (Vector2D(0,0)))
       
class Attaque2v2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque2v2")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(self.engage==0):
            self.engage=1
            if(id_team==1):
                return SoccerAction(Vector2D(0,0), (Vector2D((GAME_WIDTH)/3, GAME_HEIGHT/2) - s.player).normalize().scale(4.5))
            return SoccerAction(Vector2D(0,0), (Vector2D((GAME_WIDTH)*2/3, GAME_HEIGHT/2) - s.player).normalize().scale(4.5))
        
        
        if(s.dir_ball.norm < 10):
            if(s.dir_ball.norm < CAN_SHOOT):
                if(id_team==1):
                    if(s.ball.x < GAME_WIDTH/2):
                        return SoccerAction(s.dir_ball.normalize().scale(3.0),  Vector2D(1,0).normalize().scale(50.0))
                if(s.ball.x > GAME_WIDTH/2):
                    return SoccerAction(s.dir_ball.normalize().scale(3.0),  Vector2D(-1,0).normalize().scale(50.0))
            return SoccerAction(s.dir_ball, (Vector2D(0,0)))
        
        if (id_team==1):
            direction = Vector2D(GAME_WIDTH/2 - s.player.x -2 , (GAME_HEIGHT*2)/3 - s.player.y).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))
        elif (id_team==2):
            direction = (Vector2D((GAME_WIDTH)/2 - s.player.x + 2, (GAME_HEIGHT)/3 - s.player.y)).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))

class Defense2v2(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defense2v2")
        self.engage = 0
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if((s.ball_vitesse.norm==0)):
            self.engage=0
        if(self.engage==0):
            self.engage=1
            if(id_team==1):
                return SoccerAction(Vector2D(0,0), (Vector2D((GAME_WIDTH)/3, GAME_HEIGHT/2) - s.player).normalize().scale(3.8))
            return SoccerAction(Vector2D(0,0), (Vector2D((GAME_WIDTH)*2/3, GAME_HEIGHT/2) - s.player).normalize().scale(3.8))
        

        if (s.ball.x > GAME_WIDTH/2 and id_team==1):
            direction = Vector2D(GAME_WIDTH/3 - s.player.x , GAME_HEIGHT/2- s.player.y).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))
        elif (s.ball.x < GAME_WIDTH/2 and id_team==2):
            direction = (Vector2D((GAME_WIDTH)*2/3, GAME_HEIGHT/2) - s.player).normalize().scale(5.0)
            return SoccerAction(direction, Vector2D(0,0))

            
        if(s.dir_ball.norm < CAN_SHOOT):
            return SoccerAction(s.dir_ball.normalize().scale(5.0), (s.joueur_proche_a(id_team, id_player).position - s.player).normalize().scale(s.eloignement((s.joueur_proche_a(id_team, id_player).position.distance(s.player)))))
            
        return SoccerAction(s.dir_ball, (Vector2D(0,0)))
