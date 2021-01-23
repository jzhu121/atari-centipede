''' Author: Jennifer Zhu
    Updated: Jan 22, 2021
    Desc: A remake of Atari Centipede.
    
    Points awarded:
        Centipede: 50
        Spider: 600
        Flea: 200
        Scorpion: 1000
        Mushroom: 1
        Regenerating mushroom: 5
    
    Rows and columns:
        rows = tuple(range(10, 640, 20))
        cols = tuple(range(10, 480, 20))
'''

# I - Import and Initialize
import os
import pygame, random, sprites
pygame.init()
pygame.mixer.init()

def showMenu(leadScore, highScore):
    '''This function defines a game loop for the menu screen of the game. It
    takes the top score on the leaderboard (int) and the player's personal
    highscore (int) as parameters. It returns a boolean indicating whether or
    not to quit the game, and a configuration of mushrooms (sprite group).'''
    # Display
    screen = pygame.display.set_mode((480, 640)) # 24 cols, 32 rows (each col/row 20 px wide)
    pygame.display.set_caption("Atari Centipede")
    
    # Entities
    cwd = os.getcwd()
    background = pygame.image.load("images/crystal-cave.jpg")
    background = background.convert()
    screen.blit(background, (0, 0))
    quitMsgFont = pygame.font.Font("Eater.ttf", 25)
    
    # Music
    pygame.mixer.music.load("sounds/Adrian von Ziegler - Evocation (Chiptune).mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    # Instantiate Sprites
    # Text
    title = sprites.Text("Centipede", (screen.get_width()/2, 200), 70, (0,255,0))
    leadScoreMsg = sprites.Text("Leaderboard: "+str(leadScore), (screen.get_width()/2, 275), 25)
    highScoreMsg = sprites.Text("Your highscore: "+str(highScore), (screen.get_width()/2, 315), 25)
    startMsg = sprites.Text("Press Space to start", (screen.get_width()/2, 575), 25)
    
    menuText = pygame.sprite.Group(title, leadScoreMsg, highScoreMsg, startMsg)
    
    # Other
    centipedes = pygame.sprite.Group()
    for i in range(12):
        centipedes.add(sprites.Centipede(i*-20+10, 4))
    
    mushrooms = pygame.sprite.Group()
    for i in range(20):
        xPos = random.randrange(30, 460, 20)
        yPos = random.randrange(30, 620, 20)          
        mushrooms.add(sprites.Mushroom((xPos, yPos)))
    
    spiders = pygame.sprite.Group()
    
    # All sprites
    allSprites = pygame.sprite.OrderedUpdates(centipedes, mushrooms, spiders, menuText)
    
    # ACTION
    
    # Assign
    keepGoing = True
    quitGame = False
    clock = pygame.time.Clock()
    
    # variables to keep track of the spider
    spiderDeathTime = pygame.time.get_ticks()
    
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                quitGame = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                keepGoing = False
        
        # Kill or instantiate spiders if necessary
        if spiders:
            for spy in spiders:
                if spy.rect.left < 0 or spy.rect.left > screen.get_width():
                    # kill if they have gone off the screen
                    spy.kill()
                    spiderDeathTime = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - spiderDeathTime >= 5000:
                # instantiate if 5 seconds have passed since their death
                spiders.add(sprites.Spider(screen, 4))
                allSprites = pygame.sprite.OrderedUpdates(centipedes, mushrooms, spiders, menuText)
    
        # Collision Detection
        # Centipedes + Mushrooms: make centipede go down
        for cent in centipedes:
            mushroomsHit = pygame.sprite.spritecollide(cent, mushrooms, False)
            for mush in mushroomsHit:
                cent.goDown()
        
        # Refresh screen
        allSprites.clear(screen, background)
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    if quitGame:
        # Display quit message
        thanks = quitMsgFont.render("Thank You for Playing!", True, (255,0,255))
        screen.blit(thanks, (75, 340))
        
        # If the player got a score greater than 0, add it to the leaderboard
        if highScore:
            leaderboard = open("leaderboard.txt", "a")
            leaderboard.write(str(highScore)+"\n")
            leaderboard.close()
            msgPt1 = quitMsgFont.render("Your Score has been added", True, (255,0,255))
            msgPt2 = quitMsgFont.render("to the leaderboard.", True, (255,0,255))
            screen.blit(msgPt1, (40, 375))
            screen.blit(msgPt2, (90, 405))
        
        pygame.display.flip()
        pygame.mixer.music.fadeout(3000)
        pygame.time.delay(3500)
    
    return quitGame, mushrooms

def playGame(mushrooms, leadScore):
    '''This function defines the main game loop of the game. It takes a
    configuration of mushrooms (sprite group) and the top score on the
    leaderboard (int) as parameters. It returns the player's score (int).'''
    # Display
    screen = pygame.display.set_mode((480, 640)) # 24 cols, 32 rows (each col/row 20 px wide)
    pygame.display.set_caption("Atari Centipede")
    
    # Entities
    background = pygame.image.load("images/crystal-cave.jpg")
    background = background.convert()
    screen.blit(background, (0, 0))
    
    gameOverFont = pygame.font.Font("Eater.ttf", 50)
    
    # Music and Sound Effects
    pygame.mixer.music.load("sounds/Adrian von Ziegler - Evocation (Chiptune).mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # When a laser is shot
    shoot = pygame.mixer.Sound("sounds/shoot.wav")
    shoot.set_volume(0.4)
    # When a centipede is hit
    splat = pygame.mixer.Sound("sounds/splat.wav")
    splat.set_volume(1)    
    # When any other enemy is hit
    hit = pygame.mixer.Sound("sounds/hit.wav")
    hit.set_volume(0.9)    
    # When the player loses a life
    buzzer = pygame.mixer.Sound("sounds/buzzer.wav")
    buzzer.set_volume(1)       
    
    # Instantiate Sprites
    player = sprites.Player()
    scoreKeeper = sprites.Counter("Score", 0, 10)
    lifeKeeper = sprites.Counter("Lives", 3, 360)
    leadingScore = sprites.Text(str(leadScore), (screen.get_width()/2, 20), 25)
    
    centipedes = pygame.sprite.Group()
    for i in range(12):
        centipedes.add(sprites.Centipede(i*-20+10, 4))
    
    spiders = pygame.sprite.Group()
    fleas = pygame.sprite.Group()
    scorpions = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
        
    # All sprites
    allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
    
    # ACTION
    
    # Assign
    keepGoing = True
    clock = pygame.time.Clock()
    rows = tuple(range(10, 640, 20))
    firingRate = 500  # how many miliseconds must pass between shots
    
    # variables to keep track of periodic events
    centipedeDeathTime = pygame.time.get_ticks()
    spiderDeathTime = pygame.time.get_ticks()
    fleaDeathTime = pygame.time.get_ticks()
    scorpionDeathTime = pygame.time.get_ticks()
    shootTime = pygame.time.get_ticks()
    
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        # WASD and arrow keys move the player
        if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            player.setDirection((0,1))
        elif pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            player.setDirection((0,-1))
        elif pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            player.setDirection((-1,0))
        elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.setDirection((1,0))
        else:
            player.setDirection((0,0))

        # Space shoots lasers
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if pygame.time.get_ticks() - shootTime >= firingRate:
                laser = sprites.Laser(player.rect.centerx, player.rect.top)
                lasers.add(laser)
                shootTime = pygame.time.get_ticks()
                allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
                shoot.play()

        
        # Update enemy sprites (kill or instantiate centipedes, spiders, fleas and scorpions)
        if not centipedes and (pygame.time.get_ticks() - centipedeDeathTime >= 1500):
            # If 1.5 seconds have passed since the centipedes died, spawn a new centipede
            for i in range(12):
                centipedes.add(sprites.Centipede(i*-20+10, 4)) # speed must be a factor of 20
            allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
        
        if spiders:
            for spy in spiders:
                if spy.rect.left < 0 or spy.rect.left > screen.get_width():
                    # kill if they have gone off the screen
                    spy.kill()
                    spiderDeathTime = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - spiderDeathTime >= 5000:
                # instantiate if 5 seconds have passed since their death
                spiders.add(sprites.Spider(screen, 4))
                allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
        
        if fleas:
            for flea in fleas:
                if flea.rect.centery in rows and random.randrange(15) == 0:
                    # if flea is on a row, there is a 1 in 15 chance it will leave a mushroom behind
                    mush = sprites.Mushroom(flea.rect.center)
                    mushrooms.add(mush)
                    allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
                
                if flea.rect.top > screen.get_height():
                    # kill if they have gone off the screen
                    flea.kill()
                    fleaDeathTime = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - fleaDeathTime >= 7000:
                # instantiate if 7 seconds have passed since their death
                fleas.add(sprites.Flea(5))
                allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
        
        if scorpions:
            for scor in scorpions:
                if scor.rect.right < 0 or scor.rect.left > screen.get_width():
                    # kill if they have gone off the screen
                    scor.kill()
                    scorpionDeathTime = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - scorpionDeathTime >= 6000:
                # instantiate if 6 seconds have passed since their death
                scorpions.add(sprites.Scorpion(screen))
                allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
                
        # Collision Detection
        # Lasers + ...
        for l in lasers:
            # ...Centipedes: kill both, spawn mushroom, score 50 pts
            centipedesHit = pygame.sprite.spritecollide(l, centipedes, False)
            for cent in centipedesHit:
                splat.play()
                scoreKeeper.setCount(50)
                cent.kill()
                l.kill()
                mush = sprites.Mushroom(cent.rect.center)
                mushrooms.add(mush)
                allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
                if not centipedes:
                    centipedeDeathTime = pygame.time.get_ticks()
            
            # ...Mushrooms: kill laser, damage mushroom, maybe score 1 pt
            mushroomsHit = pygame.sprite.spritecollide(l, mushrooms, False)
            for mush in mushroomsHit:
                l.kill()
                mush.setHealth(mush.getHealth()-1)
                if mush.getHealth() == 0:
                    scoreKeeper.setCount(1)
            
            # ...Spiders: kill both, score 600 pts
            spidersHit = pygame.sprite.spritecollide(l, spiders, False)
            for spy in spidersHit:
                hit.play()
                l.kill()
                spy.kill()
                spiderDeathTime = pygame.time.get_ticks()
                scoreKeeper.setCount(600)
            
            # ...Fleas: kill both, score 200 pts
            fleasHit = pygame.sprite.spritecollide(l, fleas, False)
            for flea in fleasHit:
                hit.play()
                l.kill()
                flea.kill()
                fleaDeathTime = pygame.time.get_ticks()
                scoreKeeper.setCount(200)
            
            # ...Scorpions: kill both, score 1000 pts
            scorpionsHit = pygame.sprite.spritecollide(l, scorpions, False)
            for scor in scorpionsHit:
                hit.play()
                l.kill()
                scor.kill()
                scorpionDeathTime = pygame.time.get_ticks()
                scoreKeeper.setCount(1000)                   
        
        # Mushrooms + ...
        for mush in mushrooms:
            # ...Centipedes: make centipede go down
            centipedesHit = pygame.sprite.spritecollide(mush, centipedes, False)
            for cent in centipedesHit:
                cent.goDown()
                if mush.getIsPoisonous():
                    cent.setIsPoisoned(True)
            
            # ...Spiders: 1/3 chance of killing mushroom
            spidersHit = pygame.sprite.spritecollide(mush, spiders, False)
            for spy in spidersHit:
                if random.randrange(3) == 0:
                    mush.kill()
            
            # ...Scorpions: turn mushroom poisonous
            scorpionsHit = pygame.sprite.spritecollide(mush, scorpions, False)
            for scor in scorpionsHit:
                mush.setIsPoisonous(True)
        
        # Player + Centipedes or Spiders or Fleas: lose life, reset screen
        if pygame.sprite.spritecollide(player, centipedes, False) or pygame.sprite.spritecollide(player, spiders, False) or pygame.sprite.spritecollide(player, fleas, False):
            # Lose a life
            lifeKeeper.setCount(-1)
            buzzer.play()
            if lifeKeeper.getCount() <= 0:
                keepGoing = False
            pygame.time.delay(1000)
            
            # Heal and award 5 points for any damaged mushrooms
            # Also revert poisoned mushrooms to normal
            for mush in mushrooms:
                if mush.getHealth() < 4:
                    mush.setHealth(4)
                    scoreKeeper.setCount(5)
                if mush.getIsPoisonous():
                    mush.setIsPoisonous(False)
            
            # Reset screen:
            # Kill all enemy sprites
            for cent in centipedes:
                cent.kill()
            
            for spy in spiders:
                spy.kill()
            spiderDeathTime = pygame.time.get_ticks()
            
            for flea in fleas:
                flea.kill()
            fleaDeathTime = pygame.time.get_ticks()
            
            for scor in scorpions:
                scor.kill()
            scorpionDeathTime = pygame.time.get_ticks()
            
            # Spawn new centipede
            for i in range(12):
                centipedes.add(sprites.Centipede(i*-20+10, 4)) # speed must be a factor of 20
            allSprites = pygame.sprite.OrderedUpdates(lasers, player, centipedes, mushrooms, scorpions, spiders, fleas, scoreKeeper, lifeKeeper, leadingScore)
        
        # Refresh screen
        allSprites.clear(screen, background)
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    
    # Display Game Over message and fade out music
    gameOver = gameOverFont.render("GAME OVER", True, (255, 0, 255))
    
    # Blit the messages
    screen.blit(gameOver, (90, 230))
    pygame.display.flip()
    
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2000)
    
    return scoreKeeper.getCount()

def main():
    '''This function defines the 'mainline logic' of the program.'''
    # Read the highest score on the leaderboard
    try:
        leaderboard = open("leaderboard.txt", "r")
        leadScore = 0
        for line in leaderboard:
            if int(line) > leadScore:
                leadScore = int(line)
        leaderboard.close()
    
    except FileNotFoundError:
        leadScore = 0
    
    # Game loops
    quitGame = False
    highScore = 0
    while not quitGame:
        quitGame, mushrooms = showMenu(leadScore, highScore)
        if quitGame:
            break
        highScore = max(playGame(mushrooms, leadScore), highScore)
    
    # Close the game window
    pygame.quit()    

# Call the main function
main()
