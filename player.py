from token import Token


#Player class defines the properties and behaviours of a player
class Player():

    def __init__(self, gameSetup, color, basePosition, diceBackground):
        self.color = color
        self.basePosition = basePosition
        self.diceBackground = diceBackground
        self.tokens = []

        #represent how many tokens at the end
        self.atEnd = 0
        #represent which place the player won
        self.place = None

        #these two attributes are for creating a linked list with other players
        self.nextPlayer = None
        self.previousPlayer = None

        #to help determine the action status of the player
        self.anotherMove = True

        #finally, initialize 4 tokens.
        for i in range(4):
            self.tokens.append(Token(gameSetup, color, i))
    

    #this function is used to create a linked list
    def addPlayer(self, nextPlayer):
        self.nextPlayer = nextPlayer
        nextPlayer.previousPlayer = self


    #returns whether the player can make any further actions
    #false if the player is not eligible for making a move, or cannot make a valid move with their tokens
    def action(self, diceValue):

        if not self.anotherMove:
            return False
        
        for token in self.tokens:
            if token.isValid(diceValue):
                return True
            
        return False
        