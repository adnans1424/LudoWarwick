import pygame
from mytoken import Token


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

        #to create a computer player
        self.automized = False

        #finally, initialize 4 tokens.
        for i in range(4):
            self.tokens.append(Token(gameSetup, color, i))
    

    #this function is used to create a linked list
    def addPlayer(self, nextPlayer):
        self.nextPlayer = nextPlayer
        nextPlayer.previousPlayer = self


    #returns whether the player can make any further actions
    #false if the player is not eligible for making a move, or cannot make a valid move with their tokens
    def actionsAvailable(self, diceValue):

        if not self.anotherMove:
            return False
        
        for token in self.tokens:
            if token.isValid(diceValue):
                return True
            
        return False
        
    
    #this is an algorithm designed to make a decision on which token to play for the computer player
    def play(self, screen, dice):
        
        #to sort the four tokens from furthest to closest to base
        Player.mergeSort(self.tokens)

        #roll the dice
        pygame.time.wait(800)
        dice.getRandom(screen)

        #to eliminate invalid tokens
        validTokens = []
        for token in self.tokens:
            if token.isValid(dice.outcome):
                validTokens.append(token)


        #here is the algorithm (for more details, look at the project report)

        #is dice 6?
        if dice.outcome == 6:
            for token in validTokens:
                #is there any token at the base?
                if token.current == 0:
                    token.move(self, dice)
                    return

        
        for token in validTokens:
            #is there any token that can move to a safe square?
            try:
                if token.path[token.current + dice.outcome].safe and (token.current + dice.outcome) < 52:
                    token.move(self, dice)
                    return
            except:
                pass
            
        
        for token in validTokens:
            #is there any token that can capture another token?
            try:
                if token.path[token.current + dice.outcome].tokens[0].color != token.color:
                    token.move(self, dice)
                    return
            except:
                pass


        for token in validTokens:
            #is there any token that can reach the end square?
            if token.current + dice.outcome == 57:
                token.move(self, dice)
                return
            

        for token in validTokens:
            #are all tokens in a safe square?
            if not token.path[token.current].safe:
                token.move(self, dice)
                return
            

        for token in validTokens:
            #if the token moves, will be the 7 squares behind safe?
            empty = True
            try:
                for i in range(7):
                    for otherToken in token.path[token.current + dice.outcome - i].tokens:
                        if otherToken.color != token.color:
                            empty = False #make it false once one other token is found
                            break
                    
                    if not empty: #this is only to double break from the loop
                        break

                if empty:
                    token.move(self, dice)
                    return
                
            except:
                pass


        #move the closest token, which is the last in the list
        try:
            validTokens[len(validTokens)-1].move(self, dice)
        except:
            pass

    
    #this is a static function that uses merge sort to sort the tokens from furthest to closest
    def mergeSort(tokens):

        #when reaching the end of the recursion
        if len(tokens) == 1:
            return
        
        counter = 0

        #split into two lists
        tokens1 = tokens[:len(tokens)//2]
        tokens2 = tokens[len(tokens)//2:]

        #sort each list
        Player.mergeSort(tokens1)
        Player.mergeSort(tokens2)

        #given that both lists are sorted, we can compare element by element starting from the begining
        i=0; j=0
        while i < len(tokens1) and j < len(tokens2):

            if tokens1[i].current > tokens2[j].current:
                tokens[counter] = tokens1[i]
                i += 1
                counter += 1
            else:
                tokens[counter] = tokens2[j]
                j += 1
                counter += 1

        #if there is a small difference between the length of the lists
        while i < len(tokens1):

            tokens[counter] = tokens1[i]
            i += 1
            counter += 1

        while j < len(tokens2):

            tokens[counter] = tokens2[j]
            j += 1
            counter += 1