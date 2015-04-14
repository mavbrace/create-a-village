import pygame, sys, eztext
from peoplemake import createRandomPerson,run_simulation
from pygame.locals import *
import random


pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,200,0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
BROWN = (156,106,65)

screen_width = 800
screen_height= 600
gameDisplay = pygame.display.set_mode([screen_width,screen_height])
clock = pygame.time.Clock()

class PersonSprite(pygame.sprite.Sprite):
    def __init__(self):
 
        # Call the parent class (Sprite) constructor
        super(PersonSprite, self).__init__()
 
        #an image loaded from the disk***.
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        self.image = pygame.image.load("look.png").convert()
        self.image.set_colorkey(WHITE)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.being = None

    def generate_random(self):
        self.being = createRandomPerson()

    def add_being(self,being):
        self.being = being

class HouseSprite(pygame.sprite.Sprite):
    def __init__(self,colour,width,height):
        super(HouseSprite, self).__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        

def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def game_continue(people,records,houses):

    #load mouse-over image for the being
    over_image = pygame.image.load("look2.png").convert()
    
    sprites_list = pygame.sprite.Group()
    houses_list = pygame.sprite.Group()

    messages = ["...","...","...","...","...","..."]
    
    #------display all living sprites
    #limit, for now, to 200
    limit = 0
    for person in people:
        if limit == 200:
            break;
        person_sprite = PersonSprite()
        person_sprite.add_being(person)
        #set random location...
        person_sprite.rect.x = random.randrange(175,screen_width-20)
        person_sprite.rect.y = random.randrange(0,screen_height-60)
        #add 'person_sprite' to list of sprites
        sprites_list.add(person_sprite)
        limit += 1
    #----------------
    for i in range(houses):
        house_sprite = HouseSprite(BROWN,50,40)
        #set location...
        house_sprite.rect.x = random.randrange(175,screen_width-20)
        house_sprite.rect.y = random.randrange(0,screen_height-60)
        #add 'house_sprite' to list of sprites
        houses_list.add(house_sprite)   
        
    cont = True
    while cont:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.fill(WHITE)

        #draw all house sprites
        houses_list.draw(gameDisplay)

        #draw all people sprites
        sprites_list.draw(gameDisplay)

        for one in sprites_list:
            x = one.rect.x
            y = one.rect.y
            w = one.rect.w
            h = one.rect.h
            person = button2(x,y,w,h,return_one,one,over_image)
            if person != None:
                messages[0] = person.being.name
                messages[1] = str(person.being.age)
                messages[2] = person.being.gender
                messages[3] = person.being.hair + ", " + person.being.hairtype + " hair"
                messages[4] = person.being.skin + " skin"
                messages[5] = person.being.nose + " nose"
                
        display_text(messages,100,0,50,20)

        pygame.display.update()
            
        clock.tick(30)
        



def years_to_pass(people):
    
    yearLoop = True
    records = []

    #prompt message:
    message = ["Please enter the","number of years","that will pass"]
    
    prompter = ">>>"
    yearBox = eztext.Input(maxlength=3,color=BLACK,prompt=prompter,
                         restricted="1234567890",font=pygame.font.Font("freesansbold.ttf",15))
    yearBox.set_pos(40,85+len(message)*15)

    
    while yearLoop:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_RETURN and yearBox.value != "":
                    years = yearBox.value
                    yearLoop = False

            gameDisplay.fill(WHITE)

            display_text(message,100,0,70,15)

            yearBox.update(events)
            yearBox.draw(gameDisplay)
    
            pygame.display.update()
            
            clock.tick(30)

    print(years)
    people,records,houses = run_simulation(int(years),people,records)

    game_continue(people,records,houses)
    
    

#display text! --messages is an array
def display_text(messages,x,x_offset,y,y_offset):
    for i in range(len(messages)):
        msg = pygame.font.Font("freesansbold.ttf",15)
        TextSurf,TextRect = text_objects(messages[i], msg)
        TextRect.center = (x+x_offset*i,y+y_offset*i)
        gameDisplay.blit(TextSurf,TextRect)

                   
#display all sprites (the people) and ask how many years you want to pass
def action():   
    sprites_list = pygame.sprite.Group()

    #load mouse-over image for the being
    over_image = pygame.image.load("look2.png").convert()

    people = []
    #create 8 original people
    for i in range(8):
        orig_person = PersonSprite()
        orig_person.generate_random()
        #set random location...
        orig_person.rect.x = random.randrange(180,screen_width-10)
        orig_person.rect.y = random.randrange(90,screen_height-50)
        #add 'orig_person' to list of sprites
        sprites_list.add(orig_person)
        #add being (the Object "Person") to list of people
        people.append(orig_person.being)

    play = True
    messages = ["...","...","...","...","...","..."]
    while play:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        gameDisplay.fill(WHITE)
        #draw all sprites
        sprites_list.draw(gameDisplay)

        #the back button
        button(42,500,120,50,RED,BRIGHT_RED,game_intro,"Go Back",None)

        #the continue button
        button(42,400,120,50,GREEN,BRIGHT_GREEN,years_to_pass,"Continue",people)

        for one in sprites_list:
            x = one.rect.x
            y = one.rect.y
            w = one.rect.w
            h = one.rect.h
            person = button2(x,y,w,h,return_one,one,over_image)
            if person != None:
                messages[0] = person.being.name
                messages[1] = str(person.being.age)
                messages[2] = person.being.gender
                messages[3] = person.being.hair + ", " + person.being.hairtype + " hair"
                messages[4] = person.being.skin + " skin"
                messages[5] = person.being.nose + " nose"
                
        display_text(messages,100,0,50,20)

        #pygame.display.flip()
        pygame.display.update()
        clock.tick(15)

        

def return_one(one):
    return one

def tester():
    print("TEST")
    
        
#buttons for any occasion! ic and ac are colours
def button(x,y,w,h,ic,ac,method,message,extra_object):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y: #location of button
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0] == 1 and method != None: #if it's been clicked
            if extra_object != None:
                method(extra_object)
            else:
                method()
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    msgText = pygame.font.Font("freesansbold.ttf",15)
    textSurf,textRect = text_objects(message,msgText)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(textSurf,textRect)

#buttons without colours! Images, that is!
def button2(x,y,w,h,method,one,img):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y: #location of button
        img.set_colorkey(WHITE)
        gameDisplay.blit(img,(x,y,w,h))
      
        
        if click[0] == 1 and method != None: #if it's been clicked
            test = method(one)
            return test
    else:
        return None




def game_intro():

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        gameDisplay.fill(WHITE)
        largeText = pygame.font.Font("freesansbold.ttf",90)
        TextSurf,TextRect = text_objects("Begin:", largeText)
        TextRect.center = ((screen_width/2),(screen_height/2))
        gameDisplay.blit(TextSurf,TextRect)

        button(350,400,100,50,GREEN,BRIGHT_GREEN,action,"",None)

        pygame.display.update()
        clock.tick(15)
        
def main():
    game_intro()

	
main()
	
