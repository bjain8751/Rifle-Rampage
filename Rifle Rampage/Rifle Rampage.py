#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 11:31:25 2020

@author: bhaveshjain
"""
#importing libraries
import pygame
import time
import random
from pygame import mixer


pygame.init()

#main screen
main_screen=pygame.display.set_mode((800,600))
run=True
bg=pygame.image.load("background3.jpg")
pygame.display.set_caption("Rifle Rampage")
logo=pygame.image.load('duel.png')
pygame.display.set_icon(logo)





#gun
gun_img=pygame.image.load("gun.png")
gun_x=700
gun_y=270
gun_change_y=0
def showgun(x,y):
    main_screen.blit(gun_img, (x,y))
    
#bullet 
bullet_img=pygame.image.load("bullet.png")
bullet_x=700
bullet_y=0
bullet_change_x=15  
bullet_status="ready"
def bulletfire(x,y):
    main_screen.blit(bullet_img,(x-10,y+16))
    

#terrorist
terrorist_img=[]
terrorist_x=[]
terrorist_y=[]
terrorist_change_y=[5,5,5,5,5]
#we have 5 terrorists
for i in range(5):
    terrorist_img.append(pygame.image.load("terrorist.png"))
    terrorist_x.append((random.randint(50, 200)))    
    terrorist_y.append((random.randint(60, 536)))
def showterrorist(x,y,i):
    main_screen.blit(terrorist_img[i], (x,y))
    


#kill
def kill(x1,y1,x2,y2):
    distance=((x2-x1)**2 + (y2-y1)**2)**0.5
    if distance<27:
        return True
    else:
        return False


#scoring
score=0
score_display= pygame.font.Font(('freesansbold.ttf'), 32)

def showscore(x,y):
    text=score_display.render("SCORE:"+ str(score), True, (255,255,255)) 
    main_screen.blit(text, (x,y))

start=time.time()
end=time.time()

font_time= pygame.font.Font(('freesansbold.ttf'), 32)

def timer(x,y):
    if end-start<60:
        
        font_times= font_time.render("TIME:"+str(60-int(end-start)),True,(255,255,255))
    else:
        font_times= font_time.render("TIME:0",True,(255,255,255))
    main_screen.blit(font_times, (x,y))
    
gameover=pygame.font.Font(("freesansbold.ttf"), 64)

def endgame(x,y):
    over=gameover.render("GAME OVER",True,(255,0,0))
    main_screen.blit(over, (x,y))

f=open("scores.txt","a+")
once=1
highscore=0
scores=[]
font_score=pygame.font.Font(("freesansbold.ttf"), 32)
def showhighscore(x,y):
    hs=font_score.render("HIGH SCORE : "+str(highscore),True,(255,0,0))
    main_screen.blit(hs, (x,y))




#game body  
while run:
    main_screen.fill((0,0,0))
    main_screen.blit(bg,(0,0))
    
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run=False
        #movement of gun
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
                gun_change_y=10
            if event.key==pygame.K_UP:
                gun_change_y=-10
            if event.key==pygame.K_SPACE and bullet_status=="ready":
                bullet_y=gun_y
                bullet_status="fire"
                (mixer.Sound('laser.wav')).play()
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                gun_change_y=0
    
    
    #gun movement
    gun_y+= gun_change_y
    if gun_y<60:
        gun_y=60
    if gun_y>536:
        gun_y=536 
        
   
    #bullet
    if bullet_status=="fire":
        bulletfire(bullet_x, bullet_y)
        bullet_x -= bullet_change_x
    if bullet_x< 0:
        bullet_status="ready"
        bullet_x=700
    
    end=time.time()
     
    # terrorist 
    if end-start<60:    
        for i in range(5):
            terrorist_y[i]+=terrorist_change_y[i]
            if terrorist_y[i]>536 or terrorist_y[i]<60:
                terrorist_x[i]+=50
                terrorist_change_y[i] *= -1
            if terrorist_x[i]>300:
                terrorist_x[i]=50
    else:
        for i in range(5):
            terrorist_y[i]=2000
        endgame(200, 250)
        if once==1:
            once=0
            f.write(str(score)+"\n")
            f.flush()
            f.seek(0)
            for i in f:
                scores.append(int(i))
            highscore=max(scores)
        showhighscore(270, 330)
          
        
    #kill
    for i in range(5):
        if kill(bullet_x,bullet_y,terrorist_x[i],terrorist_y[i]):
            bullet_x=700
            bullet_status="ready"
            score+=1
            (mixer.Sound('explosion.wav')).play()
            terrorist_x[i]=((random.randint(50, 200)))    
            terrorist_y[i]=((random.randint(60, 536)))
            break
            
    
    end=time.time( )
        
    for i in range(5):
       showterrorist(terrorist_x[i], terrorist_y[i], i)
    showgun(gun_x, gun_y)
    timer(660,10)
    showscore(10, 10)
    pygame.display.update()
    
