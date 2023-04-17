#Square class defines the properties and behaviours of a square in the gameboard
#a Square object is only responsible for rendering images on it
class Square():

    def __init__(self, position, safe=False):
        self.position = position
        #some squares in the gameboard are safe, as they prevent capturing
        self.safe = safe
        #a Square object keeps track of the tokens in it, so it can render the images of the tokens correctly
        self.tokens = []

    #to add a token to the list
    def addToken(self, token):
        self.tokens.append(token)
        token.changePosition(self.position)

    #to remove a token from the list
    def removeToken(self, token):
        self.tokens.remove(token)

    #to render images on the square
    def renderImage(self, gameSetup, screen):

        if self.tokens:

            #to make it easier to track the number of tokens of each color, we creat a dictionary,
            #where keys represents the color, and its value represents the number of tokens of that color
            track = {}
            for token in self.tokens:
                if token.color in track:
                    track[token.color] += 1
                else:
                    track[token.color] = 1




            #if it is a safe square, then it is possible for differently-colored tokens to coexist,
            #therefore, if different colors coexist, we must render a small image of the tokens
            if self.safe and len(track.keys()) > 1:
                for color, quantity in track.items():
                    screen.blit(gameSetup.images[color][quantity - 1][1], self.position)

            #otherwise, render the regular size
            else:
                for color, quantity in track.items():
                    screen.blit(gameSetup.images[color][quantity - 1][0], self.position)

            #(for more details on accessing token images, look at creator.py)
