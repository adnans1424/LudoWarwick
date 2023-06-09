from button import Button


#Token class defines the properties and behaviours of a token
#a Token object inherits Button class, because a token is clickable as a button
class Token(Button):

    #a counter to keep track of the order of winners (Ludo has three winners)
    winnerPlace = 0

    def __init__(self, gameSetup, color, tokenNumber):

        self.color = color
        #path is a list of Square, which the token must go through in order to reach the end
        self.path = gameSetup.getPath(color, tokenNumber)
        #all tokens start at the base
        self.current = 0


        super().__init__(self.path[self.current].position, (37,37))
        

        #token must add itself to the square, on which, it exists
        self.path[self.current].addToken(self)


    #this function moves the token to a different square, and apply the rules of the game
    def move(self, player, dice):

        player.anotherMove = False
        steps = dice.outcome

        #per game rules, first move must be one step
        if self.current == 0:
            steps = 1
        
        #the token must remove itself from the old square
        self.path[self.current].removeToken(self)

        #move
        self.current += steps
        
        #capture other tokens if possible, and if so, the player is eligible for another move
        if self.capture():
            dice.makeAvailable(player)

        #if the dice value is 6, the player is eligible for another move
        if dice.outcome == 6:
            dice.makeAvailable(player)

        #if the token reaches the end, the player is eligible for another move, or the player wins if all tokens are at the end
        if self.finished():

            player.atEnd += 1

            if player.atEnd < 4:
                dice.makeAvailable(player)

            else:
                player.place = Token.winnerPlace
                Token.winnerPlace += 1 #increment the value for next winner

                #this will remove the current player from the linked list
                #remove the references to the current player from neighbour players on the list
                player.previousPlayer.nextPlayer = player.nextPlayer
                player.nextPlayer.previousPlayer = player.previousPlayer

        #finally, the token must add itself to the new square
        self.path[self.current].addToken(self)


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

        if diceValue == 0:
            return False
        
        #if it is at the begining and the dice value is not 6
        if self.current == 0 and diceValue != 6:
            return False
        
        #if the dice value is greater than the remaining path
        if (57 - self.current) < diceValue:
            return False
        
        return True
