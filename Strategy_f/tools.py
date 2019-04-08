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

GAME_WIDTH = 150
GAME_HEIGHT = 90
PLAYER_RADIUS = 1.
BALL_RADIUS = 0.65
CAN_SHOOT = PLAYER_RADIUS + BALL_RADIUS


class SuperState(SoccerState):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        self.counter = 0
    
    def __getattr__(self, attr):
        return getattr(self.state, attr)
    
    def add_counter(self):
        self.counter = self.counter + 1

    @property
    def ball(self):
        return self.state.ball.position
    
    @property
    def ball_vitesse(self):
        return self.state.ball.vitesse
    
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
    @property
    def player_e(self):
        return self.state.player_state(self.det_team_e(self.id_team), self.id_player).position
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
        return self.ball - self.player
    
    @property
    def dir_ball_vitesse(self):
        if(self.ball.y + self.state.ball.vitesse.y < 0):
            return Vector2D(self.ball.x + self.state.ball.vitesse.x , 5) - self.player
        if(self.ball.y + self.state.ball.vitesse.y > GAME_HEIGHT):
            return Vector2D(self.ball.x + self.state.ball.vitesse.x , GAME_HEIGHT-5) - self.player
        if(self.ball.x + self.state.ball.vitesse.x < 0):
            return Vector2D(5, self.ball.y + self.state.ball.vitesse.y) - self.player
        if(self.ball.x + self.state.ball.vitesse.x > GAME_WIDTH):
            return Vector2D(GAME_WIDTH - 5, self.ball.y + self.state.ball.vitesse.y) - self.player
        return self.ball - self.player
    
    @property
    def dir_point(self, vec):
        return self.state.position - vec
    
    def distance_balle(self, pointB, distance):
        return (self.state.ball.position.distance(pointB) < distance)
    
    def distance_avec_balle(self):
        return (self.state.ball.position.distance(self.state.player_state(self.id_team, self.id_player).position))
    
    def det_team(self, nb):
        if(nb == 0):
            return 1
        return -1
    
    def det_team_e(self, nb):
        if(nb == 1):
            return 2
        return 1
    def eloignement(self, nb):
        return(math.log1p(nb*0.6))

    @property
    def dir_ball_acc(self):
        """direction vers balle + acceleration de balle"""

#        return ((self.distance_avec_balle() * self.state.ball.vitesse + self.state.ball.position) - self.state.player_state(self.id_team, self.id_player).position).normalize().scale(5)
        a=self.dir_ball.norm * 5
        return ((a*self.state.ball.vitesse + self.state.ball.position) - self.state.player_state(self.id_team, self.id_player).position).normalize().scale(5)
    
    
    def joueur_proche(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if (id_player != self.id_player or id_team != self.id_team)]
        return min([(self.player.distance(player_p.position), player_p) for player_p in opponents])[1]
        try:
            a=min([(self.player.distance(player_p.position), player_p) for player_p in opponents])[1]
        except TypeError:
            a=self.state.player_state(self.det_team_e(id_team),0)
        return a


    def joueur_proche_a(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if id_team == self.id_team and id_player != self.id_player]
        return min([(self.player.distance(player_a.position), player_a) for player_a in opponents])[1]
        try:
            a=min([(self.player.distance(player_a.position), player_a) for player_a in opponents])[1]
        except TypeError:
            a=self.state.player_state(self.det_team_e(id_team),0)
        return a
    
    def joueur_proche_ball_all(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players]
        try:
            a=min([(self.ball.distance(player_e.position), player_e) for player_e in opponents])[1]
        except TypeError:
            a=self.state.player_state(self.det_team_e(id_team),0)
        return a
        
    def joueur_proche_ball_a(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if id_team == self.id_team and id_player != self.id_player]
        try:
            a=min([(self.ball.distance(player_e.position), player_e) for player_e in opponents])[1]
        except TypeError:
            a=self.state.player_state(self.det_team_e(id_team),0)
        return a
        
    def joueur_e(self, id_team, id_player):
        return self.state.player_state(self.det_team_e(id_team), self.id_player).position
    
    def joueur_solo_attaque(self, id_team):
        if(self.player.distance(Vector2D(self.player.x, self.joueur_e(self.det_team_e(id_team), 0).position.y)) < self.joueur_e(self.det_team_e(id_team), 0).distance(Vector2D(self.player.x, self.joueur_e(self.det_team_e(id_team), 0)).position.y)):
            return 1
    
    def test_joueur_e(self, id_team, id_player, joueur):
        team_e = self.det_team_e(id_team)
        for i in range(id_player):
            if(joueur==self.state.player_state(team_e, i)):
                return i
    
    
    
    
    def passe(self, Vector):
        return Vector.normalize().scale(2.5)
    
    def shoot(self, Vector):
        return Vector.normalize().scale(3.8)
    
    
def frange(start, stop, step):
     i = start
     while i < stop:
         yield i
         i += step

    
    
class GoTestStrategy(Strategy):
    def __init__(self, strength=None):
        Strategy.__init__(self, "Go-getter")
        self.strength = strength
    
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        if(s.dir_ball.norm < CAN_SHOOT):
                return SoccerAction(s.dir_ball, (s.goal_e - s.player).normalize().scale(3.8))
        return SoccerAction(s.dir_ball.normalize().scale(4), Vector2D(0, 0))
 
class GoTestSolo(Strategy):
    def __init__(self, strength=None):
        Strategy.__init__(self, "Solo")
        self.counter = 0
        self.counterstep = 0
        self.strength = strength
    
    def compute_strategy(self, state, id_team, id_player):
        if(state.step==0):
            self.counterstep = 0
            self.counter = 0
            
        self.counterstep += 1
        s = SuperState(state, id_team, id_player)
        dir_balle = s.ball - s.player
#        Distance_Shoot = (s.ball - s.player).norm 
        pos_cible = ((s.ball - s.goal_a)/2 + (s.goal_a - s.player)).scale(3.8)
        
        if(s.ball.x == GAME_WIDTH/2 and s.ball.y == GAME_HEIGHT/2):
            self.counter = 0
            
        if(self.counter == 1):
            if(dir_balle.norm < CAN_SHOOT):
                return SoccerAction(dir_balle, (s.goal_e - s.player).normalize().scale(3.8))
            return SoccerAction(dir_balle, Vector2D(0, 0))
        
        
        if(self.counterstep >= 500):
            if(dir_balle.norm < CAN_SHOOT):
                return SoccerAction(dir_balle, (s.goal_e - s.player).normalize().scale(3.8))
            return SoccerAction(dir_balle, Vector2D(0, 0))
        
        
        if(id_team==1):
            if((s.ball - s.player).norm + (s.ball - s.goal_e).norm < (s.ball - s.joueur_e(id_team, id_player)).norm + (s.ball - s.goal_e).norm and (s.player.x > s.joueur_e(id_team, id_player).x)):
                if(dir_balle.norm < CAN_SHOOT):
                    self.counterstep = 0
                    self.counter = 1
                    return SoccerAction(dir_balle, (s.goal_e - s.player).normalize().scale(3.8))
                if(s.distance_balle(s.player, 10)):
                    return SoccerAction(dir_balle, Vector2D(0., 0.))
                return SoccerAction(pos_cible, Vector2D(0,0))
            
        if(id_team==2):
           if((s.ball - s.player).norm + (s.ball - s.goal_e).norm < (s.ball - s.joueur_e(id_team, id_player)).norm + (s.ball - s.goal_e).norm and (s.player.x < s.joueur_e(id_team, id_player).x)):
               if(dir_balle.norm < CAN_SHOOT):
                   self.counterstep = 0
                   self.counter = 1
                   return SoccerAction(dir_balle, (s.goal_e - s.player).normalize().scale(3.8))
               if(s.distance_balle(s.player, 10)):
                   return SoccerAction(dir_balle, Vector2D(0., 0.))
               return SoccerAction(pos_cible, Vector2D(0,0))
           
    
        if(s.distance_balle(s.player, CAN_SHOOT)):
            if(s.dir_ball.norm < CAN_SHOOT):
                self.counterstep = 0
                if(s.player.x < GAME_WIDTH*0.5 and s.player.y < GAME_HEIGHT*0.5): #en bas à gauche
                    return SoccerAction(dir_balle,(Vector2D(0,0)-s.player).normalize().scale(3.8))
                if(s.player.x < GAME_WIDTH*0.5 and s.player.y > GAME_HEIGHT*0.5): #en haut à gauche
                    return SoccerAction(dir_balle,(Vector2D(0,GAME_HEIGHT)-s.player).normalize().scale(3.8))
                if(s.player.x > GAME_WIDTH*0.5 and s.player.y > GAME_HEIGHT*0.5): #en haut à droite
                    return SoccerAction(dir_balle,(Vector2D(GAME_WIDTH,GAME_HEIGHT)-s.player).normalize().scale(3.8))
                if(s.player.x > GAME_WIDTH*0.5 and s.player.y < GAME_HEIGHT*0.5): #en bas à droite
                    return SoccerAction(dir_balle,(Vector2D(GAME_WIDTH,0)-s.player).normalize().scale(3.8))
                if(s.joueur_e(id_team, id_player).y > s.player.y):
                    return SoccerAction(dir_balle, (Vector2D(0, -GAME_HEIGHT).normalize().scale(3.8)))
                return SoccerAction(dir_balle, Vector2D(0, GAME_HEIGHT).normalize().scale(2.5))
            return SoccerAction(dir_balle, Vector2D(0,0))
            
        # id_team is 1 or 2
        # id_player starts at 0
        

        if(s.distance_balle(s.player, 10)):
            return SoccerAction(dir_balle, Vector2D(0., 0.))
        return SoccerAction(pos_cible, Vector2D(0,0))

