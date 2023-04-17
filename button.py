#Button class defines the properties and behaviours of a button
class Button():

    def __init__(self, position, dimensions, image=None, imageBig=None, imageDim=None):
        self.image = image
        self.imageBig = imageBig
        self.imageDim = imageDim

        self.dimensions = dimensions

        #position represent the position of the left upper corner
        self.position = position
        #opposite position represent the position of the right bottom corner,
        self.oppositePosition = (position[0] + dimensions[0], position[1] + dimensions[1])


    #this function render the image of the button
    def update(self, screen, mousePosition, mouseInput):

        #button appearance changes depending on the mouse pointer
        #if the button is pressed, it appears dim
        if self.isHovering(mousePosition) and self.isPressed(mouseInput):
            screen.blit(self.imageDim, self.position)
        
        #if the button is pointed at but not pressed, it appears large
        elif self.isHovering(mousePosition):
            screen.blit(self.imageBig, self.position)

        #or appears normally otherwise
        else:
            screen.blit(self.image, self.position)


    #this function returns whether the mouse is pointing at the button
    def isHovering(self, mousePosition):

        #using the position and opposite position, we can determine the area of the button,
        #and then determine whether the mouse pointer is positioned on the button
        if mousePosition[0] in range(self.position[0], self.oppositePosition[0]) and mousePosition[1] in range(self.position[1], self.oppositePosition[1]):
            return True
        
        return False
    
    
    #this function returns whether the mouse is pressing the button
    def isPressed(self, mouseInput):

        if mouseInput[0] is True:
            return True
        
        return False
    