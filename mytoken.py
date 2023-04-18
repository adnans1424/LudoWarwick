import pygame
from button import Button


#Token class defines the properties and behaviours of a token
#a Token object inherits Button class, because a token is clickable as a button
class Token(Button):

    def __init__(self, gameSetup, color, tokenNumber):

        self.color = color
        #path is a list of Square, which the token must go through in order to reach the end
        self.path = gameSetup.getPath(color, tokenNumber)
        #all tokens start at the base
        self.current = 0


        super().__init__(self.path[self.current].position, (37,37))
        

        #token must add itself to the square, on which, it exists
        self.path[self.current].addToken(self)


    #this function moves the token to a different square, and returns whether it captured another token there.
    def move(self, screen, steps):

        #per game rules, first move must be one step
        if self.current == 0:
            steps = 1
        
        #the token must remove itself from the old square
        self.path[self.current].removeToken(self)

        for i in range(steps):

            # start = self.path[self.current].position
            # end = self.path[self.current + 1].position

            # xDistance = end[0] - start[0]
            # yDistance = end[1] - start[1]

            # xVelocity = xDistance / 50
            # yVelecity = yDistance / 50

            # for i in range(50):
            #     screen.blit(self.images[0][0], (start[0] + xVelocity, start[1] + yVelecity))
            #     pygame.display.flip()
            #     clock.tick(50)

            

            self.current += 1


        #capture another token if possible
        captured = self.capture()

        #finally, the token must add itself to the new square
        self.path[self.current].addToken(self)

        return captured


    #this function tries to capture other tokens if possible, and returns whether it did
    def capture(self):

        captured = False

        #these are all the condition, in which capturing is not possible (safe square, empty square, same color tokens)
        #reminder: in a non-safe square, it is not possible for different colors to coexist
        if self.path[self.current].safe or not self.path[self.current].tokens or self.path[self.current].tokens[0].color == self.color:
            return captured

        #in this loop, all other tokens will be put back in their base
        while self.path[self.current].tokens:

            otherToken = self.path[self.current].tokens[0]

            otherToken.current = 0
            otherToken.path[otherToken.current].addToken(otherToken)
            self.path[self.current].removeToken(otherToken)

            captured = True

        return captured
    
    
    #this function returns whether the token has reached the end
    def finished(self):
        return self.current == 57


    #this function changes the attribute of the position of the token
    def changePosition(self, newPosition):
        self.position = newPosition
        self.oppositePosition = (self.position[0] + self.dimensions[0], self.position[1] + self.dimensions[1])

    
    #this function returns whether this token has any valid moves based on the dice value
    def isValid(self, diceValue):
        
        #if it is at the begining and the dice value is not 6
        if self.current == 0 and diceValue != 6:
            return False
        
        #if the dice value is greater than the remaining path
        if (57 - self.current) < diceValue:
            return False
        
        return True
