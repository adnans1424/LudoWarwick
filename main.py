import pygame
from pygame.image import load
from button import Button
from dice import Dice
from creator import TokenCreator
from player import Player
dir = "GameAssets/{}.png"
flag = 0
# flag = pygame.FULLSCREEN | pygame.SCALED


#game setup
pygame.init()
#A Clock object is used to control the framerate
clock = pygame.time.Clock()
#screen is used to display graphics on the window (800px * 800px)
screen = pygame.display.set_mode((800, 800), flags = flag)


#After the initialization, the game is devided into functions, where
#each function has its own game loop. This method helps organizing
#game screens. For example, we start with main menu screen, then
#go to the game screen by calling game(4).




#this is the main menu screen in which we start our game and end it
def mainMenu():

    #before the game loop, we load the game data needed
    #background image
    mainMenu = load(dir.format("main_menu_background"))
    #Button objects
    onePlayerButton = Button((208, 250), (385, 110), load(dir.format("computer_button_small")),
                                                      load(dir.format("computer_button_big")),
                                                      load(dir.format("computer_button_big_dim")))
    twoPlayersButton = Button((208, 380), (385, 110), load(dir.format("2players_button_small")),
                                                      load(dir.format("2players_button_big")),
                                                      load(dir.format("2players_button_big_dim")))
    fourPlayersButton = Button((208, 510), (385, 110), load(dir.format("4players_button_small")),
                                                       load(dir.format("4players_button_big")),
                                                       load(dir.format("4players_button_big_dim")))


    #game loop
    while True:
        #dispaly the main menu background
        screen.blit(mainMenu, (0,0))


        #since Button objects interact with the mouse pointer, we need to store its data (it is used only for graphics)
        mouseInput = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        
        #render the graphics of the buttons on the screen
        onePlayerButton.update(screen, mousePosition, mouseInput)
        twoPlayersButton.update(screen, mousePosition, mouseInput)
        fourPlayersButton.update(screen, mousePosition, mouseInput)



        #pygame.event.get() returns a list that contains any new interactions with the game.
        #Thus, the code here is resposible for game response to player's action
        for event in pygame.event.get():

            #if the user clicks X or ESC, it will exit the main menu and quit the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == 27):
                return

            #if the user clicks while hovering on the buttons, it will enter the game screen.
            if event.type == pygame.MOUSEBUTTONUP and onePlayerButton.isHovering(mousePosition):
                game(2, True)

            if event.type == pygame.MOUSEBUTTONUP and twoPlayersButton.isHovering(mousePosition):
                game(2, False)

            if event.type == pygame.MOUSEBUTTONUP and fourPlayersButton.isHovering(mousePosition):
                game(4, False)


        #to apply all changes on screen and refresh the window
        pygame.display.flip()

        #to restrict the refresh rate to 60 frames/second
        clock.tick(60)



#this is the game screen
def game(numOfPlayers, computer):
    #to create an instance for the current game set
    gameSetup = TokenCreator()


    ##### part (1): load game data before the game loop #####

    #before the game loop, we load the game data needed
    #a background image
    board = load(dir.format("game_board"))
    #Button object
    mainMenuButton = Button((15, 719), (165, 66), load(dir.format("mainmenu_button_small")),
                                                  load(dir.format("mainmenu_button_big")),
                                                  load(dir.format("mainmenu_button_big_dim")))
    #a dice
    dice = Dice()
    #a counter to keep track of the order of winners (Ludo has three winners)
    winnerPlace = 0
    #images for the winners
    awardsImages = [load(dir.format("one")), load(dir.format("two")), load(dir.format("three"))]
    
    

    #initiate 2 or 4 players (depending on the game mode) with their appropriate color and data
    players = [Player(gameSetup, "red", (121, 455), load(dir.format("red_background"))),
               Player(gameSetup, "yellow", (508, 68), load(dir.format("yellow_background")))]
    if numOfPlayers == 4:
        players.insert(1, Player(gameSetup, "blue", (121, 68), load(dir.format("blue_background"))))
        players.insert(3, Player(gameSetup, "green", (508, 455), load(dir.format("green_background"))))
    if computer: #if we are in computer mode
        players[1].automized = True


    #this creates a circular doubly linked lists, it is used to rotate turns between players,
    #and to delete a player who finished the game
    for i in range(numOfPlayers):
        players[i].nextPlayer = players[(i+1) % numOfPlayers]
        players[i].previousPlayer = players[(i-1) % numOfPlayers]

    #this variable represnt the player in the current turn
    currentPlayer = players[0]
    ########################################################





    #game loop
    while True:
        ##### part (2): refresh all graphics on screen #####

        #display the board screen
        screen.blit(board, (0,0))
        #display the current player's color behind the dice, that color helps the players to know whose turn it is
        screen.blit(currentPlayer.diceBackground, (310, 688))
        
        #as explained before, mouse data is used to help update Button objects
        mouseInput = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        
        #render the graphics of the dice and buttons on the screen
        dice.update(screen)
        mainMenuButton.update(screen, mousePosition, mouseInput)

        #render the graphics of every square on the gameboard
        for square in gameSetup.record:
            square.renderImage(gameSetup, screen, currentPlayer, dice)

        #render the awards images for the winners
        #each winner will have an award image based on their place (e.g. first place will get "first award")
        for player in players:
            #a player wins when having four tokens at the end
            if player.atEnd == 4:
                screen.blit(awardsImages[player.place], player.basePosition)
        #########################################################





        ##### part (3): check game status #####

        #in the linked list, if a player is refering to themselves, that means they are the last one
        #and they lose and game ends
        if currentPlayer == currentPlayer.nextPlayer:
            pygame.time.wait(1000)
            gameOver()
            return

        #if the current player has no more actions to make and the dice is not available, that means their turn ends
        if not currentPlayer.actionsAvailable(dice.outcome) and not dice.available:
            currentPlayer = currentPlayer.nextPlayer #go to next player's turn
            dice.makeAvailable(currentPlayer) #reset dice for the current player

            
            print("player changed")
        ##########################################################

        
        


        ##### part (4): game response for player's (or computer) action #####

        #for computer player
        if currentPlayer.automized:
            currentPlayer.play(dice)

        #for human player
        for event in pygame.event.get():
            #if a player clicks X, ESC or main menu button, it will pop up a warning message and then exit to main menu
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == 27) or (event.type == pygame.MOUSEBUTTONUP and mainMenuButton.isHovering(mousePosition)):
                if exitWarning():
                    return

            #if the dice was clicked while it is available, it will produce a random value and show it on screen
            if event.type == pygame.MOUSEBUTTONUP and dice.isHovering(mousePosition) and dice.available:
                dice.getRandom(screen)

            #to check if the current player has interacted with their tokens, we iterate through their tokens
            for token in currentPlayer.tokens:

                #if the token was clicked while the dice is NOT available and it is a valid move, that token will be played
                if event.type == pygame.MOUSEBUTTONUP and token.isHovering(mousePosition) and not dice.available and token.isValid(dice.outcome) and currentPlayer.actionsAvailable(dice.outcome):
                    
                    token.move(currentPlayer, dice.outcome, dice)

                    break
        #############################################################


        #to apply all changes on screen and refresh the window
        pygame.display.flip()

        #to restrict the refresh rate to 60 frames/second
        clock.tick(60)



#this is the exit warning screen
def exitWarning():

    #similar to main menu
    #load the game data needed
    dimming = load(dir.format("dim_background"))
    messagebox = load(dir.format("exit_warning"))
    yesButton = Button((230, 430), (165, 66), load(dir.format("yes_button_small")),
                                                  load(dir.format("yes_button_big")),
                                                  load(dir.format("yes_button_big_dim")))
    noButton = Button((405, 430), (165, 66), load(dir.format("no_button_small")),
                                                    load(dir.format("no_button_big")),
                                                    load(dir.format("no_button_big_dim")))



    #dimming effects need to be rendered once only
    screen.blit(dimming, (0,0))

    #game loop
    while True:

        #render images
        screen.blit(messagebox, (0,0))

        mouseInput = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        
        yesButton.update(screen, mousePosition, mouseInput)
        noButton.update(screen, mousePosition, mouseInput)


        for event in pygame.event.get():

            #wait for the players to confirm exiting to main menu
            if event.type == pygame.MOUSEBUTTONUP and yesButton.isHovering(mousePosition):
                return True

            if event.type == pygame.MOUSEBUTTONUP and noButton.isHovering(mousePosition):
                return False
            
        
        #refresh the window
        pygame.display.flip()
        clock.tick(60)



#this is the game over screen
def gameOver():

    #similar to main menu
    #load the game data needed
    dimming = load(dir.format("dim_background"))
    messagebox = load(dir.format("gameover"))
    mainMenuButton = Button((318, 430), (165, 66), load(dir.format("mainmenu_button_small")),
                                                  load(dir.format("mainmenu_button_big")),
                                                  load(dir.format("mainmenu_button_big_dim")))



    #dimming effects need to be rendered once only
    screen.blit(dimming, (0,0))

    #game loop
    while True:

        #render images
        screen.blit(messagebox, (0,0))

        mouseInput = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        
        mainMenuButton.update(screen, mousePosition, mouseInput)


        for event in pygame.event.get():

            #wait until the main menu button is pressed
            if event.type == pygame.MOUSEBUTTONUP and mainMenuButton.isHovering(mousePosition):
                return
            
        
        #refresh the window
        pygame.display.flip()
        clock.tick(60)    



mainMenu()

pygame.quit()