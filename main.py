import pygame
from pygame import mixer
import math
import random
from tkinter import *


def play():
    global playing
    playing = True
    screen1.destroy()


def quit():
    global playing
    playing = False
    screen1.destroy()

screen1=Tk()
screen1.title('AIR CLASH')
screen1.geometry('500x500')
welcome_text= Label(text='WELCOME TO AIR CLASH',fg='red',bg='yellow')
welcome_text.pack()
play_Button = Button(text='PLAY',fg='white',bg='black', height=5,width=20,command=play)
play_Button.place(x=180,y=100)
exit_Button = Button(text='EXIT',fg='white',bg='black', height=5,width=20,command=quit)
exit_Button.place(x=180,y=300)

screen1.mainloop()


pygame.init()

main_screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('f16.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("AIR CLASH")
icon = pygame.image.load('Spaceship.png')
pygame.display.set_icon(icon)

player_image = pygame.image.load('aircraft.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


Enemy_Image = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []


num_of_enemies = 6

for i in range(num_of_enemies):
    Enemy_Image.append(pygame.image.load('helicopter.png'))
    EnemyX.append(random.randint(0,770))
    EnemyY.append(random.randint(50,150))
    EnemyX_change.append(0.3)
    EnemyY_change.append(0.3)


Bullet_Image = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 0
BulletX_change = 0
BulletY_change = 0.8
Bullet_state = 'rest'

font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf',80)

End_Game = False
close = False
score_value = 0


def show_score(x,y):
    score = font.render('score:'+str(score_value),True,(255,255,255))
    main_screen.blit(score, (x, y))


def gameover():
    for j in range(num_of_enemies):
        EnemyY[j] = 2000
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    main_screen.blit(over_text, (200, 250))


def player(x, y):
    main_screen.blit(player_image, (x, y))


def Enemy(x, y, i):
    main_screen.blit(Enemy_Image[i], (x, y))


def Fire_Bullet(x, y):
    global Bullet_state
    Bullet_state = 'fire'
    main_screen.blit(Bullet_Image, (x, y - 20))


def collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x2-x1, 2))+(math.pow(y2-y1, 2)))
    if distance < 27:
        return True
    else:
        return False


def colide_sound():
    Collision_sound = mixer.Sound('explosion.wav')
    Collision_sound.play()


def replay():
    global explode, End_Game, playerX, playerY, score_value
    explode = not explode
    End_Game = False
    screen2.destroy()
    playerX = 370
    playerY = 480
    score_value = 0
    for a in range(num_of_enemies):
        EnemyX[a] = random.randint(0, 770)
        EnemyY[a] = random.randint(50, 150)


def exit():
    global running, playing , close
    playing = False
    running = False
    close = True
    screen2.destroy()


if playing:
    running = True
    while running:
        main_screen.fill((0, 0, 150))
        # Red, Green, Blue(0-255)
        main_screen.blit(background, (-100, -200))

#        print(playerX) # this function will show the location of our image at x axis
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if Bullet_state == 'rest':
                        Bullet_sound = mixer.Sound('laser.wav')
                        Bullet_sound.play()
                        BulletX = playerX
                        BulletY = playerY
                        Fire_Bullet(BulletX, BulletY)
                        BulletY -= BulletY_change

                if event.key == pygame.K_RIGHT:
                    playerX_change = +0.3

                if event.key == pygame.K_LEFT:
                    playerX_change = -0.3

                if event.key == pygame.K_DOWN:
                    playerY_change = +0.3
                if event.key == pygame.K_UP:
                    playerY_change = -0.3

        playerX += playerX_change
        playerY += playerY_change

        if BulletY <= 0:
            BulletY = playerY
            Bullet_state = 'rest'

        if Bullet_state == 'fire':
            Fire_Bullet(BulletX, BulletY)
            BulletY -= BulletY_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 770:
            playerX = 770

        if playerY <= 0:
            playerY = 0
        elif playerY >= 570:
            playerY = 570

        player(playerX, playerY)

        for a in range(num_of_enemies):
            EnemyX[a] += EnemyX_change[a]
            if EnemyX[a] <= 0:
                EnemyX_change[a] = 0.3
#                EnemyY[a] += EnemyY_change[a]        # for movement in x axis only
            elif EnemyX[a] >= 770:
                EnemyX_change[a] = -0.3
#                EnemyY[a] += EnemyY_change[a]      # for movement in x axis only
            EnemyY[a] += EnemyY_change[a]       # uncomment for random movement everywhere

            if EnemyY[a] <= 0:
                EnemyY_change[a] = 0.3
            elif EnemyY[a] >= 570:
                EnemyY_change[a] = -0.3

            Enemy(EnemyX[a], EnemyY[a], a)

            explode = collision(EnemyX[a], EnemyY[a], playerX, playerY)
            if explode:
                End_Game=True
                colide_sound()

            Collide = collision(EnemyX[a],EnemyY[a],BulletX,BulletY)
            if Collide:
                colide_sound()
                BulletY = 480
                Bullet_state = 'rest'
                score_value += 1
                EnemyX[a] = random.randint(0, 770)  # We have to consider the size of image as well
                EnemyY[a] = random.randint(50, 150)

            if End_Game == True:
                gameover()
                screen2 = Tk()
                screen2.title('AIR CLASH')
                screen2.geometry('500x500')
                replay_Button = Button(text='RESTART', fg='white', bg='black', height=5, width=20, command=replay)
                replay_Button.place(x=180, y=100)
                exit_Button = Button(text='EXIT', fg='white', bg='black', height=5, width=20, command=exit)
                exit_Button.place(x=180, y=300)
                Score_Label = Label(text='Your Score:' + str(score_value), font=('Arial', 16))
                Score_Label.pack()
                if not close:
                    screen2.mainloop()

        show_score(textX, textY)
        pygame.display.update()
        # It should be updated continuously
'''To change the background of our window/Anything that you want to be persistent in your game window you want it'''