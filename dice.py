import random
import pygame
from pygame.image import load
from button import Button
dir = "GameAssets/{}.png"


#Dice class defines the properties and behaviours of the dice
#a Dice object inherits Button class, because a dice is clickable as a button
class Dice(Button):

    #dice images
    faces = [load(dir.format("dice_null")),
             load(dir.format("dice_1")),
             load(dir.format("dice_2")),
             load(dir.format("dice_3")),
             load(dir.format("dice_4")),
             load(dir.format("dice_5")),
             load(dir.format("dice_6")),]
    
    
    #initialize as a button
    def __init__(self):
        super().__init__((368, 703), (65, 65))

        self.available = True
        self.outcome = 0


    #override update() function, because a dice manages its appearance differently
    #render the image corresponding to the outcome of the dice
    def update(self, screen):
        screen.blit(self.faces[self.outcome], (368, 705))


    #this function returns a randomized value for a dice
    def getRandom(self, screen):

        #the moment a dice is clicked, it disables itself, until it gets reset in the game flow
        self.available = False

        #this loop purpose is show an animation for rolling a dice, by displaying 10 random value,
        #but it only returns the last one
        for i in range(1):

            self.outcome = random.randint(1, 6)

            self.update(screen)

            pygame.display.flip()
            pygame.time.wait(150)

        return self.outcome
    

    #this function resets the dice and the current player status
    def makeAvailable(self, player):
        self.available = True
        self.outcome = 0

        player.anotherMove = True
