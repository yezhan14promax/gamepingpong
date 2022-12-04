import cv2
import random
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import pygame
import sys
from random import randint
import time


def Button(screen, position, text, bwidth=200,bheight=50):
    bouttonimage = pygame.image.load("D:\game\lol.jpeg")
    boutton = pygame.transform.scale(bouttonimage, (bwidth, bheight))
    screen.blit(boutton,position)
    font = pygame.font.Font(None, 30)
    text_render = font.render(text, 1, (238,211,196))
    left, top = position
    return screen.blit(text_render, (left+50, top+10))
    '''left, top = position
    bwidth, bheight = button_size
    pygame.draw.line(screen, (150, 150, 150), (left, top), (left+bwidth, top), 5)
    pygame.draw.line(screen, (150, 150, 150), (left, top-2), (left, top+bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left, top+bheight), (left+bwidth, top+bheight), 5)
    pygame.draw.line(screen, (50, 50, 50), (left+bwidth, top+bheight), (left+bwidth, top), 5)
    pygame.draw.rect(screen, (100, 100, 100), (left, top, bwidth, bheight))
    font = pygame.font.Font(None, 30)
    text_render = font.render(text, 1, (255, 235, 205))
    return screen.blit(text_render, (left+50, top+10))'''
def start(screen):
    clock = pygame.time.Clock()
    
    while True:
        #screen.fill('black')
        image=pygame.image.load("D:\game\gta.jpeg")
        screen.blit(image,(0,0))
        button_1 = Button(screen, (220, 75), 'Play')
        button_2 = Button(screen, (220, 175), "Histoire")
        button_3 = Button(screen, (220, 275), "Aide")
        button_4 = Button(screen, (220, 375), "Quitter")
        for event3 in pygame.event.get():
            if event3.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Cliquez sur le bouton
            if event3.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(pygame.mouse.get_pos()):
                    return run(screen)
                elif button_2.collidepoint(pygame.mouse.get_pos()):
                    return histoire(screen)
                elif button_3.collidepoint(pygame.mouse.get_pos()):
                    return aide(screen)
                elif button_4.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        clock.tick(10)
        pygame.display.update()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color,width,height):
        super().__init__()
        self.image=pygame.Surface([width,height])
        pygame.draw.rect(self.image,color,[0,0,width,height])
        self.rect=self.image.get_rect()
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.y>560:
            self.rect.y=560
    def automove(self, ball_rect_y):
        a=random.random()
        if a>=0.5:
            if ball_rect_y-self.rect.y>10:
                self.rect.y+=10
            if ball_rect_y-self.rect.y<10:
                self.rect.y-=10



class Ball(pygame.sprite.Sprite):
    def __init__(self, color,width,height):
        super().__init__()
        self.image=pygame.Surface([width,height])
        pygame.draw.rect(self.image,color,[0,0,width,height])
        self.speedx=randint(2,6)
        self.speedy=randint(2,6)
        self.rect=self.image.get_rect()

        #garder le ball hors des limites
        if self.rect.y<0:
            self.rect.y=0
        if self.rect.y>470:
            self.rect.y=470
        if self.rect.x>630:
            self.rect.x=630
        if self.rect.x<0:
            self.rect.x=0
    #mouvement
    def update(self):
        self.rect.x +=self.speedx
        self.rect.y +=self.speedy
    #collision
    def bouncing(self):
        self.speedx=-1.25*self.speedx
        self.speedy=1.15*self.speedy
  
#programme de jeu principal
def run(screen):
    cap = cv2.VideoCapture(0) #0为自己的摄像头
    detector = HandDetector(maxHands=1)
    clock=pygame.time.Clock()
    #paddle
    paddle1=Paddle('white',10,80)
    paddle1.rect.x=0
    paddle1.rect.y=200
    paddle2=Paddle('white',10,80)
    paddle2.rect.x=630
    paddle2.rect.y=200
    #ball
    ball=Ball('yellow',10,10)
    ball.rect.x=316
    ball.rect.y=236
    #add
    game_sprites=pygame.sprite.Group()
    game_sprites.add(paddle1)
    game_sprites.add(paddle2)
    game_sprites.add(ball)
    #point
    score1=0
    score2=0
    pygame.font.init()
    font3=pygame.font.Font(None,80)
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  
        hands, img = detector.findHands(img, flipType=False)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
        paddle2.automove(ball_rect_y=ball.rect.y)
        if hands:
            lmList = hands[0]['lmList']     
            pointIndex = lmList[8][0:2]     #site de index
            pointIndex = tuple(pointIndex)  
            #print(type(img))
            pointdoit = lmList[8][1:2]       #Passer les coordonnées à la raquette
            paddle1.rect.y=pointdoit[-1]
            
            cv2.circle(img, pointIndex, 20, (0, 0, 255), cv2.FILLED)
        cv2.imshow('image',img)
        
        #Dessinez l'images d'arrière-plan, le ball et des raquettes à screen
        screen.fill('black')
        image=pygame.image.load("D:\game\gta4.jpeg")
        image=pygame.transform.scale(image,(640,480))
        screen.blit(image,(0,0))
        pygame.draw.line(screen,'white',(318,0),(318,480),5)
        game_sprites.draw(screen)
        game_sprites.update()

        #Frapper et marquer
        if ball.rect.x>=630:
            ball.rect.x=630
            if pygame.sprite.collide_mask(ball,paddle2):
                ball.bouncing()
            else:
                score1=score1+1
                ball.speedx=-ball.speedx
        elif ball.rect.x<=0:
            ball.rect.x=0
            if pygame.sprite.collide_mask(ball,paddle1):
                ball.bouncing()
            else:
                score2=score2+1
                ball.speedx=-ball.speedx
        elif ball.rect.y>=470:
             ball.rect.y=470
             ball.speedy=-ball.speedy
        elif ball.rect.y<=0: 
            ball.rect.y=0 
            ball.speedy=-ball.speedy
        elif pygame.sprite.collide_mask(ball,paddle1) or pygame.sprite.collide_mask(ball,paddle2):
            ball.bouncing()
        elif score1>=5 or score2>=5:
            temps= str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            textnote='play vs ordinateur: '+str(score1)+':'+str(score2)+'    '+temps
            note3=open("D:\game\histoire.txt",mode='w')
            note3.write(textnote)
            note3.close()
            return end(screen, score1, score2)
        #afficher le score
        text=font3.render(str(score1),True,"red")
        screen.blit(text,(220,100))
        text=font3.render(str(score2),True,"red")
        screen.blit(text,(420,100))
        
        pygame.display.update()
        clock.tick(144)

def end(screen, score1, score2):
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(None,100)
    font2 = pygame.font.Font(None,35)
    msg = 'win!' if score1 > score2 else 'lost:)' 
    texts = [font1.render(msg, True,(238,211,196)),
            font2.render('Press ESCAPE to quit.', True,(246,90,64)),
            font2.render('Press ENTER to continue or play again.', True,(246,90,64))]
    positions = [[240, 200], [170, 270], [90, 300]]
    while True:
        #screen.fill('black')
        image=pygame.image.load("D:\game\end.jpeg")
        image=pygame.transform.scale(image, (640, 480))
        screen.blit(image,(0,0))
        for event0 in pygame.event.get():
            if event0.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event0.type == pygame.KEYDOWN:
                if event0.key == pygame.K_RETURN:
                    return start(screen)
                elif event0.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        for text, pos in zip(texts, positions):
            screen.blit(text, pos)
        clock.tick(10)
        pygame.display.update()

def histoire(screen):
    clock = pygame.time.Clock()
    note1 = open("D:\game\histoire.txt",'r')
    note = note1.readline()
    font = pygame.font.Font(None,30)
    texts = [font.render(str(note),True,'black'),
            font.render('Press ESC or ENTER to quit.', True,(246,90,64))]
    positions=[[85,200],[85, 300]]
    while True:
        #screen.fill('black')
        image=pygame.image.load("D:\game\end.jpeg")
        image=pygame.transform.scale(image, (640, 480))
        screen.blit(image,(0,0))
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_RETURN or event1.key == pygame.K_ESCAPE:
                    return start(screen)        
        for text, pos in zip(texts, positions):
            screen.blit(text, pos)
        clock.tick(10)
        pygame.display.update()

def aide(screen):
    clock = pygame.time.Clock()
    font1 = pygame.font.Font(None,25)
    font2 = pygame.font.Font(None,30)
    texts = [font1.render('La reconnaissance de la main contrôle la raquette gauche',True,'black'),
            font1.render('le joueur qui touche 5 points gagne',True,'black'),
            font2.render('Press ENTRE or ESC to quit.', True,(246,90,64))]
    positions = [[85,250], [140,300], [160, 350]]
    while True:
        #screen.fill('black')
        image=pygame.image.load("D:\game\end.jpeg")
        image=pygame.transform.scale(image, (640, 480))
        screen.blit(image,(0,0))
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_RETURN or event2.key == pygame.K_ESCAPE:
                    return start(screen)                 
        for text, pos in zip(texts, positions):
            screen.blit(text, pos)
        clock.tick(10)
        pygame.display.update()

def main():
    pygame.init()                                           #initialisation
    pygame.mixer.init()
    size=(640,480)
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption('jeu pong,乒乓球游戏')        #titre
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.3)                       #BGM
    pygame.mixer.music.get_volume() 
    #pygame.mixer.music.load("D:Michael Hunter - Soviet Connection (Theme from Grand Theft Auto IV).mp3")
    pygame.mixer.music.load("D:\game\Michael Hunter - Theme From San Andreas.mp3")
    pygame.mixer.music.play(-1)
    
    
    
    game_pause=True
    if game_pause==True:
        return start(screen)
    


if __name__ == '__main__':
    main()
 



        




