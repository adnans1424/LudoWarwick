from pygame.image import load
from square import Square
dir = "GameAssets/{}.png"

#TokenCreator class is responsible for creating a game setup, which all tokens can access
class TokenCreator():

    #this is a 3D array to store the image data for tokens
    #dimension: ([color of token][number of tokens][image size])
    #it has been designed this way for easy access when rendering images of tokens
    images = {"red": [[load(dir.format("red_token")), load(dir.format("red_token_small"))],
                      [load(dir.format("red2_token")), load(dir.format("red2_token_small"))],
                      [load(dir.format("red3_token")), load(dir.format("red3_token_small"))],
                      [load(dir.format("red4_token")), load(dir.format("red4_token_small"))]],

              "blue": [[load(dir.format("blue_token")), load(dir.format("blue_token_small"))],
                       [load(dir.format("blue2_token")), load(dir.format("blue2_token_small"))],
                       [load(dir.format("blue3_token")), load(dir.format("blue3_token_small"))],
                       [load(dir.format("blue4_token")), load(dir.format("blue4_token_small"))]],
                      
              "yellow": [[load(dir.format("yellow_token")), load(dir.format("yellow_token_small"))],
                         [load(dir.format("yellow2_token")), load(dir.format("yellow2_token_small"))],
                         [load(dir.format("yellow3_token")), load(dir.format("yellow3_token_small"))],
                         [load(dir.format("yellow4_token")), load(dir.format("yellow4_token_small"))]],
                         
              "green": [[load(dir.format("green_token")), load(dir.format("green_token_small"))],
                        [load(dir.format("green2_token")), load(dir.format("green2_token_small"))],
                        [load(dir.format("green3_token")), load(dir.format("green3_token_small"))],
                        [load(dir.format("green4_token")), load(dir.format("green4_token_small"))]]}
    highlight = load(dir.format("token_highlight"))
    
    #these two variables hold necessary data to initialize the tokens
    firstSquare = {"red": 0, "blue": 13, "yellow": 26, "green": 39} #the first square to start per color
    basePosition = {"red": (152, 486), "blue": (152, 99), "yellow": (539, 99), "green": (539, 486)} #the position of the base per color
    

    def __init__(self):

        #when creating a game instance, we must declare all squares, in the main array and specific-color arrays
        self.mainArray = [Square((339, 587), safe=True), Square((339, 544)),            Square((339, 501)),            Square((339, 458)),
                          Square((339, 415)),            Square((296, 372)),            Square((253, 372)),            Square((210, 372)),
                          Square((167, 372), safe=True), Square((124, 372)),            Square((81, 372)),             Square((81, 329)),
                          Square((81, 286)),             Square((124, 286), safe=True), Square((167, 286)),            Square((210, 286)),
                          Square((253, 286)),            Square((296, 286)),            Square((339, 243)),            Square((339, 200)),
                          Square((339, 157)),            Square((339, 114), safe=True), Square((339, 71)),             Square((339, 28)),
                          Square((382, 28)),             Square((425, 28)),             Square((425, 71), safe=True),  Square((425, 114)),
                          Square((425, 157)),            Square((425, 200)),            Square((425, 243)),            Square((468, 286)),
                          Square((511, 286)),            Square((554, 286)),            Square((597, 286), safe=True), Square((640, 286)),
                          Square((683, 286)),            Square((683, 329)),            Square((683, 372)),            Square((640, 372), safe=True),
                          Square((597, 372)),            Square((554, 372)),            Square((511, 372)),            Square((468, 372)),
                          Square((425, 415)),            Square((425, 458)),            Square((425, 501)),            Square((425, 544), safe=True),
                          Square((425, 587)),            Square((425, 630)),            Square((382, 630)),            Square((339, 630))]
        
        self.coloredArrays = {"red": [Square((382, 587)), Square((382, 544)), Square((382, 501)), Square((382, 458)), Square((382, 415)), Square((382, 372))],
                              "yellow": [Square((382, 71)), Square((382, 114)), Square((382, 157)), Square((382, 200)), Square((382, 243)), Square((382, 286))],
                              "blue": [Square((124, 329)), Square((167, 329)), Square((210, 329)), Square((253, 329)), Square((296, 329)), Square((339, 329))],
                              "green": [Square((640, 329)), Square((597, 329)), Square((554, 329)), Square((511, 329)), Square((468, 329)), Square((425, 329))]}
        
        #here is a record for all Square object in the game
        self.record = self.mainArray + self.coloredArrays["red"] + self.coloredArrays["blue"] + self.coloredArrays["yellow"] + self.coloredArrays["green"]


    #this function creates a specific path for each token in the game
    def getPath(self, color, tokenNumber):

        #the base square
        newSquare = Square(self.getbasePosition(color, tokenNumber))
        self.record.append(newSquare)

        path = [newSquare]


        #then add the main array squares, with the correct start
        for i in range(self.firstSquare[color], self.firstSquare[color] + 51):
            path.append(self.mainArray[i%52])

        #then add the specific-color array
        for square in self.coloredArrays[color]:
            path.append(square)

        return path
    

    #this is a helper function to get the very specific position for each token in the base
    def getbasePosition(self, color, tokenNumber):

        xOffset = self.basePosition[color][0] + (tokenNumber//2)*73
        yOffset = self.basePosition[color][1] + (tokenNumber%2)*73

        return (xOffset, yOffset)