import random
import pygame


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1200,640))
pygame.display.set_caption('Bezdomnik Simulator')
clock = pygame.time.Clock()
running = True

#IDEAS
#Ne zaduljitelni daje tiq moje da ne gi praish:
 #promeni skachaneto na playera da moje da se zadurja

#Zaduljitelni:
 #Add god mode which will be a secret. You will have infinite money,resources and you will be able to go through walls and fly around!
 #Napravi interiora na shopa

text_font = pygame.font.SysFont('Arial',45)
text_font2 = pygame.font.SysFont('Arial',30)
text_font3 = pygame.font.Font('assets/ObelixProB-cyr.ttf',25)

def drawtext(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))

playerimage = pygame.image.load('assets/player.png')
backgroundimg = pygame.image.load('assets/bg.jpg')
background_rect = backgroundimg.get_rect(topleft=(0,0))
groundimg = pygame.image.load('assets/ground.png')
ground_rect = groundimg.get_rect(topleft=(0,595))
coiniconimg = pygame.image.load('assets/coinicon.png')
coinicon_rect = coiniconimg.get_rect(topleft=(1070,0))
cloudimg = pygame.image.load('assets/cloud.png')
cloud_rect = cloudimg.get_rect(topleft=(0,0))
trashimg = pygame.image.load('assets/trash.png')
buttonimg = pygame.image.load('assets/button.png')
yesimg = pygame.image.load('assets/yes.png')
yes_rect = yesimg.get_rect(topleft=(2000,2000))
clockiconimg = pygame.image.load('assets/clockicon.png')
clockicon_rect = clockiconimg.get_rect(topleft=(1070,80))
shopimg1 = pygame.image.load('assets/shop1.png')
shopimg2 = pygame.image.load('assets/shop2.png')

#music/sound effect loading
pygame.mixer.music.load('assets/Motion.mp3')
pygame.mixer.music.play(-1)
moneygot_sound = pygame.mixer.Sound('assets/moneygot.mp3')

#lists
clouds_x_pos = [100,300,500,700,900]

#some variables
showclockicon = False
inshop = False

#statistics
money = 0

#timers
timer1 = 0
timerstart = False
timer2 = 0
timer2start = False
timer1length = 100
timer2length = 720
timer3 = 0
timer3start = False


class Player:
    def __init__(self,speed,x,y,grav,notmove):
        self.speed = speed
        self.x = x
        self.y = y
        self.grav = grav
        self.notmove = notmove
        self.rect = playerimage.get_rect(topleft=(self.x, self.y))

    def important(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def movement(self):
        if keys[pygame.K_d] and self.notmove == False:
            self.x += self.speed
        if keys[pygame.K_a] and self.notmove == False:
            self.x -= self.speed
        #barriers
        if self.x < -20:
            self.x = -20
        if self.x > 1145:
            self.x = 1145

        if self.x > 289 and self.x < 301 and self.y == 480 and inshop == False:
            self.x = 290
        if self.x > 389 and self.x < 401 and self.y == 480 and inshop == False:
            self.x = 400

        if 839 < self.x and 851 > self.x and self.y == 480 and inshop == False:
            self.x = 840
        if 964 < self.x and 974 > self.x and self.y == 480 and inshop == False:
            self.x = 975



    def gravity(self):
        self.grav += 1
        self.y += self.grav
        if self.y > 480:
            self.y = 480
            self.grav = 0

        #collision stuff
        if 300 < self.x and 391 > self.x:
            if self.y == 395 and inshop == False:
                self.grav = -1

        if 851 < self.x and 966 > self.x:
            if self.y == 395:
                self.y = 405
            if self.y == 405 and inshop == False:
                self.grav = -1
    


            


        


class Trash:
    def __init__(self,x,y,collided):
        self.x = x
        self.y = y
        self.collided = collided
        self.rect = trashimg.get_rect(topleft=(self.x,self.y))

    def important2(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def collisioncheck(self):
        if self.rect.colliderect(player1.rect):
            self.collided = True
        else:
            self.collided = False


class QuestionPopUp:
    def __init__(self,x,y,text_x,text_y,text):
        self.x = x
        self.y = y
        self.text_x = text_x
        self.text_y = text_y
        self.text = text
        self.rect = buttonimg.get_rect(topleft=(self.x,self.y))

    def important3(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Shop:
    def __init__(self,x,y,types,collided):   
        self.x = x
        self.y = y
        self.types = types
        self.collided = collided
        self.rect = shopimg1.get_rect(topleft=(self.x,self.y))

    def important4(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def type(self):
        if self.types == 1:
            self.rect = shopimg1.get_rect(topleft=(self.x,self.y))
            if inshop == False:
                screen.blit(shopimg1,self.rect)

        if self.types == 2:
            self.rect = shopimg2.get_rect(topleft=(self.x,self.y))
            if inshop == False:
                screen.blit(shopimg2,self.rect)

    def collidecheck(self):
        if player1.rect.colliderect(self.rect):
            self.collided = True
        else:
            self.collided = False
    



#object defining
player1 = Player(10,10,480,0,False)

trash1 = Trash(320,475,False)

button1 = QuestionPopUp(400,300,385,320,'Would you like to interact with the trash?')
button2 = QuestionPopUp(400,300,430,320,'Would you like to enter the shop?')

shop1 = Shop(900,520,1,False)




while running:
    keys = pygame.key.get_pressed()
    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #player1 ground jumping code
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player1.rect.colliderect(ground_rect) and player1.notmove == False:
                player1.grav -= 20
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player1.rect.colliderect(trash1.rect):
                if 300 < player1.x and 391 > player1.x:
                    if player1.y == 395:
                        player1.grav -= 20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player1.rect.colliderect(shop1.rect):
                if 851 < player1.x and 966 > player1.x:
                    if player1.y == 405:
                        player1.grav -= 20
                
        
        #question popup1 yes button script:
        if yes_rect.collidepoint(mousepos) and player1.notmove == False and player1.rect.colliderect(trash1.rect):
            if pygame.mouse.get_pressed()[0] == 1 and timer2 == 0:
                randomcash = random.random()
                randomcash = random.randint(1,5)
                player1.notmove = True
                player1.x += 50
                money += randomcash
                moneygot_sound.play()         
                timerstart = True
                timer2start = True
                timer3start = True

        if yes_rect.collidepoint(mousepos) and player1.notmove == False and player1.rect.colliderect(shop1.rect):
            if pygame.mouse.get_pressed()[0] == 1:           
                inshop = True

  

    #player functions
    player1.important()
    player1.movement()
    player1.gravity()

    #trash functions
    trash1.collisioncheck()
    trash1.important2()

    #popup functions
    button1.important3()
    button2.important3()

    #shop functions
    shop1.important4()
    shop1.collidecheck()




    pygame.display.flip()
    screen.fill((0,0,0))
    if inshop == False:
        screen.blit(backgroundimg,background_rect)
        screen.blit(groundimg,ground_rect)
    screen.blit(playerimage,player1.rect)
    screen.blit(coiniconimg,coinicon_rect)
    if inshop == False:
        screen.blit(trashimg,trash1.rect)
    #function for drawing the specific image for the shop type
    shop1.type()

    for cloudpos1 in clouds_x_pos:
        if inshop == False:
            cloud_rect.x = cloudpos1
            screen.blit(cloudimg,cloud_rect)
    drawtext(str(money),text_font,(0,0,0),1145,14)

    #collision stuff
    if trash1.collided == True and player1.x == 290 and inshop == False:
        #these 2 lines will display the button and it's text
        screen.blit(buttonimg,button1.rect)
        drawtext(str(button1.text),text_font2,(0,0,0),button1.text_x,button1.text_y)
        #bonus 3 line for yes
        screen.blit(yesimg,yes_rect)
        yes_rect.x = 590
        yes_rect.y = 365

    if shop1.collided == True and inshop == False:
        screen.blit(buttonimg,button2.rect)
        drawtext(str(button2.text),text_font2,(0,0,0),button2.text_x,button2.text_y)
        screen.blit(yesimg,yes_rect)
        yes_rect.x = 590
        yes_rect.y = 365


    

    #checking if the player is in the shop
    if inshop == True:
        print("The player entered the shop")

    #timers/cooldowns
    if timer3start == True:
        timer3 += 1
        drawtext('You found ' + str(randomcash) + ' coins in the trash',text_font3,(255,244,67),35,180)

    if showclockicon == True:
        screen.blit(clockiconimg,clockicon_rect)

    if timer3 == 130:
        timer3 = 0
        timer3start = False

    if timer2start == True:
        showclockicon = True
        timer2 += 1

    if timer2 == timer2length:
        timer2 = 0
        timer2start = False
        showclockicon = False

    if timerstart == True:
        timer1 += 1

    if timer1 == timer1length:
        player1.x -= 50
        player1.notmove = False
        timerstart = False
        timer1 = 0

    #fps capper
    clock.tick(60)

    #print function debugging
    print(player1.y)
   
