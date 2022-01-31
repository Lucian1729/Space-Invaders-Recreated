#Python for Computational Problem Solving: Mini Project
#GUI: Coded by Nimit Mann(SRN: PES1202100653)
#Game mechanics, effects and animations: Coded by Nischal H S(SRN: PES1202100756)


import pygame
import random
import time
from pygame import mixer

try:
    from tkinter import *
    from tkinter import ttk
except:  # incase import does not work
    from Tkinter import *
    from Tkinter import ttk

#SQL
import csv

def insertIntoLog(name, score):
    file = open("scores.csv", "a+")
    writer = csv.writer(file)
    writer.writerow([name, score])

def validate(P):
    if len(P) < 15:
        #14 char or less is fine
        return True
    else:
        # Anything else, reject it
        return False



# connection = sqlite3.connect(os.getcwd() + "\\SpaceInv.db") 
# crsr = connection.cursor()

#create table if it doesn't exist
# create_command = """CREATE TABLE IF NOT EXISTS HIGHSCORE (  
# name VARCHAR(20),  
# score INT(10),    
# date DATE);"""
        
# d_command = "SELECT datetime('now','localtime');"
# crsr.execute(d_command)


# execute the statement 
# crsr.execute(create_command)

#quotes to display while game loads
quotes = [
    '"If you find yourself in a hole, the first thing to do is stop digging."\n - from Red Dead Redemption',
    '"Success is not final, failure is not fatal: \nIt is the courage to continue that counts."\n - from Call of Duty: Modern Warfare',
    '"Hope is what makes us strong. It is why we are here. \nIt is what we fight with when all else is lost."\n - from God of War 3',
    '"Reality is broken. Game designers can fix it."\n - Jane McGonigal',
    '"Games were not just a diversion, I realized. Games could make you feel."\n - Sid Meier',
    '"All our dreams can come true, if we have the courage to pursue them."\n - Walt Disney',
    '"The secret of getting ahead is getting started."\n - Mark Twain',
    '"I’ve failed over and over and over again in my\n life and that is why I succeed."\n - Michael Jordan',
    '"Don’t limit yourself. You can go as far as your mind lets you."\n - Mary Kay Ash',
    '"The best time to plant a tree was 20 years ago. \nThe second best time is now.”\n - Chinese Proverb',
    '"Only the paranoid survive.”\n - Andy Grove',
    '"Its hard to beat a person who never gives up.”\n - Babe Ruth',
    '"If people are doubting how far you can go, \ngo so far that you cant hear them anymore.”\n - Michele Ruiz',
    '"Understand that failure is not the opposite of success, it is a part of success.”\n - Arianna Huffington'
        ]

#function for main menu
def main_menu(): #window for first screen shown to user
    main = Tk()
    main.title("Python Coding Mini-Project")

    #centering
    main.update_idletasks()
    width = 750
    height = 600
    x = (main.winfo_screenwidth() // 2) - (width // 2)
    y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    main.resizable(0,0)
        
    try:
        label1 = Label(text="Welcome to Space Invaders!", font=("Century Gothic", 35), fg="black")
    except:
        label1 = Label(text="Welcome to Space Invaders!", font=("Arial", 35), fg="black")
    label1.pack(pady=30)

    def play_command_ai(): #destroys window and runs game
        global decision
        decision = "AI"
        main.destroy()
        PlayGame()
    
    def play_command_pvp(): #destroys window and runs game
        global decision
        decision = "PVP"
        main.destroy()
        PlayGame()


    button_play_ai = Button(main, text="Classic", font=("Arial", 25), width = 17, command=play_command_ai)
    button_play_ai.pack(pady=20)
    
    button_play_pvp = Button(main, text="PvP", font=("Arial", 25), width = 17, command=play_command_pvp)
    button_play_pvp.pack(pady=20)
    
    button_scores = Button(main, text="Leaderboard", font=("Arial", 25), width = 17, command=leaderboard_window)
    button_scores.pack(pady=20)

    button_quit = Button(main, text="Exit Program", font=("Arial", 25), width = 17, command=main.quit)
    button_quit.pack(pady=20)

    main.mainloop()

def loading_window(): #loading screen
    master = Tk()
    master.title("Space Invaders")
    master.attributes("-alpha", 0.0) #making window transparent before GUI loads
    master.after(0, master.attributes, "-alpha", 1.0)
    master.attributes("-topmost", True)
    #master.configure(bg="#000e20")
    master.overrideredirect(True)

    #position in centre
    master.update_idletasks()
    width = 750
    height = 600
    x = (master.winfo_screenwidth() // 2) - (width // 2)
    y = (master.winfo_screenheight() // 2) - (height // 2)
    master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    master.resizable(0,0)

    #progress text
    try: 
        progress_mainLabel = Label(master, text="Loading...", font=("Century Gothic", 40), fg="black", bd=0)
    except: 
        progress_mainLabel = Label(master, text="Loading...", font=("Arial", 40), fg="black", bd=0)
    progress_mainLabel.pack(pady=(100,10))
    quoteLabel = Label(master, text=random.choice(quotes), font=("Century Gothic", 15), fg="black", justify="center")
    quoteLabel.pack(pady=50)
    
    # defining func for progress bar
    
    def ProgressFunction(progress_current):
        try:
            progress_Progressbar["value"] = progress_current
        except:
            pass
        
    progress_max = 200
    progress_current = 0

    progress_Progressbar = ttk.Progressbar(
        master, orient="horizontal", length=300, value=progress_current, maximum=progress_max)
    progress_Progressbar.pack(pady=100)

    for i in range(1, 401):
          
        progress_current += 0.5
        progress_Progressbar.after(2, ProgressFunction(progress_current))
        progress_Progressbar.update()
    
    master.destroy()
    master.mainloop()

def user_window_ai(): #second window to input username for AI
    user = Tk()
    user.title("Classic")

    #centering
    user.update_idletasks()
    width = 750
    height = 600
    x = (user.winfo_screenwidth() // 2) - (width // 2)
    y = (user.winfo_screenheight() // 2) - (height // 2)
    user.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    user.resizable(0,0)

    label1 = Label(text="Enter your name below:", font=("Arial", 25))
    label1.pack(pady=30)

    vcmd = (user.register(validate), '%P')
    name_input = Entry(user, width=30, bd=3, insertontime=10, insertofftime=50, highlightthickness=0, validate= "key", validatecommand=vcmd)
    name_input.pack()

    def ai_game():
        pygame.init()

        screen = pygame.display.set_mode((800, 600))

        pygame.display.set_caption("Space Invaders - Classic")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)

        clock = pygame.time.Clock()

        backgroundImg = pygame.image.load('background.png')

        mixer.music.load('game_music.wav')
        mixer.music.play(-1)

        game_state = True

        playerImg = pygame.image.load('spaceship2.png')
        playerX = 368
        playerY = 480
        playerX_change = 0
        playerRect = pygame.Rect(playerX, playerY, 64, 64)

        enemyX = []
        enemyY = []
        enemyX_change = []
        enemyY_change = []
        enemyRect = []
        enemyImg1 = pygame.image.load('enemy1.png')
        enemyImg2 = pygame.image.load('enemy2.png')
        enemy_number = 10
        enemy_state = 1
        for i in range(enemy_number):
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(8)
            enemyY_change.append(40)
            enemyRect.append(pygame.Rect(enemyX[i], enemyY[i], 64, 64))
        movement_state = True
        movement_count = 1

        bulletImg = pygame.image.load('missile.png')
        bulletX = []
        bulletY = []
        bulletRect = []
        bulletY_change = 20
        bullet_sound = mixer.Sound('shoot.wav')
        fire_delay = 0
        last_fire_delay = -20

        explosionImg = pygame.image.load('explosion1.png')
        explosionX = 0
        explosionY = 0
        explosion_frames = 12
        explosion_count = 13
        collision_sound = mixer.Sound('explosion.wav')

        score_value = 0
        score_font = pygame.font.Font('game_over.ttf', 48)
        score_font_over = pygame.font.Font('game_over.ttf', 100)

        over_font = pygame.font.Font('game_over.ttf', 200)
        exit_font = pygame.font.Font('game_over.ttf', 48)

        def game_over():
            over_object = over_font.render("GAME OVER", True, (128, 0, 0))
            screen.blit(over_object, (160, 200))
            exit_object = exit_font.render("Press ESCAPE key to exit.", True, (255, 255, 255))
            screen.blit(exit_object, (290, 550))

        def score():
            if game_state:
                score_object = score_font.render("Score : " + str(score_value), True, (128, 0, 0))
                screen.blit(score_object, (10, 10))
            else:
                score_object = score_font_over.render("Score : " + str(score_value), True, (255, 255, 255))
                screen.blit(score_object, (320, 300))

        def player(x, y):
            screen.blit(playerImg, (x, y))

        def enemy(x, y, z):
            if z:
                screen.blit(enemyImg1, (x, y))
            else:
                screen.blit(enemyImg2, (x, y))

        def fire_bullet(x, y):
            bulletX.append(x + 24)
            bulletY.append(y - 20)
            bulletRect.append(pygame.Rect(x + 24, y - 20, 16, 16))

        def bullet(x, y):
            screen.blit(bulletImg, (x, y))

        def explosion(x, y):
            screen.blit(explosionImg, (x, y))

        start_time = time.time()
        end_time = start_time

        running = True
        while running:
            screen.blit(backgroundImg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -10
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 10
                    if event.key == pygame.K_SPACE:
                        if fire_delay > (last_fire_delay + 20):
                            fire_bullet(playerX, playerY)
                            bullet_sound.play()
                            last_fire_delay = fire_delay
                    if event.key == pygame.K_ESCAPE:
                        if not game_state:
                            running = False
                if event.type == pygame.KEYUP:
                    playerX_change = 0
            if game_state:
                fire_delay += 1
                end_time = time.time()

            playerX += playerX_change
            if playerX < 0:
                playerX = 0
            if playerX > 736:
                playerX = 736

            for i in range(enemy_number):
                if playerRect.colliderect(enemyRect[i]):
                    game_over()

                    game_state = False
                    for ene in range(enemy_number):
                        if enemyY[0] < 1000:
                            mixer.music.pause()
                            game_over_sound = mixer.Sound('game_over_sound.wav')
                            game_over_sound.play()
                        enemyY[ene] = 2000
                if enemyY[i] > 1000:
                    game_over()

                enemyX[i] += enemyX_change[i]
                if enemyX[i] < 0:
                    enemyX_change[i] = -enemyX_change[i]
                    enemyY[i] += enemyY_change[i]
                if enemyX[i] > 736:
                    enemyX_change[i] = -enemyX_change[i]
                    enemyY[i] += enemyY_change[i]
                enemyRect[i] = pygame.Rect(enemyX[i], enemyY[i], 64, 64)

                enemy(enemyX[i], enemyY[i], movement_state)

            if movement_count % 16 == 0:
                movement_state = not movement_state
                movement_count = 1
            movement_count += 1

            s = False
            l = len(bulletY)
            i = 0
            while i < l:
                bulletY1 = bulletY
                bulletX1 = bulletX

                bullet(bulletX[i], bulletY[i])
                bulletY[i] -= bulletY_change
                bulletRect[i] = pygame.Rect(bulletX[i], bulletY[i], 16, 16)
                for en in range(enemy_number):
                    if enemyRect[en].colliderect(bulletRect[i]):
                        explosionX = enemyX[en]
                        explosionY = enemyY[en]
                        explosion_count = 0

                        enemyX[en] = random.randint(0, 736)
                        enemyY[en] = random.randint(50, 150)

                        bulletY1.pop(i)
                        bulletX1.pop(i)

                        score_value += 1

                        collision_sound.play()

                        s = True
                        l -= 1
                        i -= 1
                        # If bullet collides with 2 enemies in same frame, will be popped twice and may cause index error.
                        # Hence must use break.
                        break
                i += 1
            if s:
                bulletY = bulletY1
                bulletX = bulletX1

            bulletY = [i for i in bulletY if i > -32]
            if len(bulletY) < len(bulletX):
                bulletX.pop(0)
                bulletRect.pop(0)

            if explosion_frames > explosion_count:
                explosion(explosionX, explosionY)
            explosion_count += 1

            player(playerX, playerY)
            playerRect = pygame.Rect(playerX, playerY, 64, 64)

            score()

            pygame.display.update()

            clock.tick(60)

        return score_value

    def save_input():
        game_name = name_input.get()
          
        display_name_label = Label(user, text="Welcome {}! Click below to start playing.".format(game_name), font=("Arial", 15))
        display_name_label.pack(pady=10)

        def play_command():
            user.destroy()
            game_score = ai_game()
            insertIntoLog(game_name, game_score)


        button_play = Button(user, text="Play Now", font=("Arial", 25), command=play_command)
        button_play.pack(pady=20)

        controls_label = Label(user, text="Controls: →/← to move right/left, space to shoot.", font=("Arial", 15))
        controls_label.pack()
    
    save_button = Button(user, text="Save", font=("Arial", 15), command=save_input)
    save_button.pack(pady=15)
    
def user_window_pvp(): #second window to input usernames of players for PVP

    user = Tk()
    user.title("Player vs Player (1v1)")

    #centering
    user.update_idletasks()
    width = 750
    height = 600
    x = (user.winfo_screenwidth() // 2) - (width // 2)
    y = (user.winfo_screenheight() // 2) - (height // 2)
    user.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    user.resizable(0,0)

    label1 = Label(user, text="Enter player 1 username below:", font=("Arial", 25))
    label1.pack(pady=30)

    vcmd = (user.register(validate), '%P')
    name1_input = Entry(user, width=30, bd=3, insertontime=10, insertofftime=50, highlightthickness=0, validate="key", validatecommand=vcmd)
    name1_input.pack()

    label2 = Label(user, text="Enter player 2 username below:", font=("Arial", 25))
    label2.pack(pady=30)

    vcmd = (user.register(validate), '%P')
    name2_input = Entry(user, width=30, bd=3, insertontime=10, insertofftime=50, highlightthickness=0, validate="key", validatecommand=vcmd)
    name2_input.pack()

    def pvp_game(name_1, name_2):
        pygame.init()

        screen = pygame.display.set_mode((800, 600))

        pygame.display.set_caption("Space Invaders - PvP")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)

        clock = pygame.time.Clock()

        backgroundImg = pygame.image.load('background2.png')

        mixer.music.load('game_music.wav')
        mixer.music.play(-1)

        game_state = True

        red = (255, 0, 0)
        green = (0, 255, 0)

        versus_font = pygame.font.Font('game_over.ttf', 80)

        player1Name = name_1
        player1Img = pygame.image.load('spaceship2white.png')
        player1Health = 40
        player1X = 32
        player1Y = 268
        player1Y_change = 0
        player1Rect = pygame.Rect(player1X, player1Y, 64, 64)

        player2Name = name_2
        player2Img = pygame.image.load('spaceship2black.png')
        player2Health = 40
        player2X = 704
        player2Y = 268
        player2Y_change = 0
        player2Rect = pygame.Rect(player2X, player2Y, 64, 64)

        bullet_sound = mixer.Sound('shoot.wav')
        bullet1Img = pygame.image.load('bullet1.png')
        bullet1X = []
        bullet1Y = []
        bullet1Rect = []
        bullet1X_change = 20
        fire_delay1 = 0
        last_fire_delay1 = -20

        bullet2Img = pygame.image.load('bullet2.png')
        bullet2X = []
        bullet2Y = []
        bullet2Rect = []
        bullet2X_change = 20
        fire_delay2 = 0
        last_fire_delay2 = -20

        collision_sound = mixer.Sound('explosion.wav')

        over_font = pygame.font.Font('game_over.ttf', 120)
        exit_font = pygame.font.Font('game_over.ttf', 48)

        def player(x, y, playerImg):
            screen.blit(playerImg, (x, y))

        def fire_bullet1(x, y):
            bullet1X.append(x + 20)
            bullet1Y.append(y + 24)
            bullet1Rect.append(pygame.Rect(x + 20, y + 24, 16, 16))

        def fire_bullet2(x, y):
            bullet2X.append(x - 20)
            bullet2Y.append(y + 24)
            bullet2Rect.append(pygame.Rect(x + 24, y + 24, 16, 16))

        def bullet1(x, y):
            screen.blit(bullet1Img, (x, y))

        def bullet2(x, y):
            screen.blit(bullet2Img, (x, y))

        def winner(x):
            if x == player1Name:
                end_colour = (255, 255, 255)
            elif x == player2Name:
                end_colour = (0, 0, 0)
            over_text = x + " wins!"
            over_object = over_font.render(over_text, True, end_colour)
            center_over_text = over_object.get_rect(center=(400, 250))
            screen.blit(over_object, center_over_text)
            exit_object = exit_font.render("Press ESCAPE key to exit.", True, (255, 255, 255))
            screen.blit(exit_object, (290, 550))

        top_text = player1Name + "  VS  " + player2Name
        top_rect = versus_font.render(top_text, True, (255, 255, 255))
        center_top_text = top_rect.get_rect(center=(400, 20))

        running = True
        while running:
            screen.blit(backgroundImg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player2Y_change = 10
                    if event.key == pygame.K_UP:
                        player2Y_change = -10
                    if event.key == pygame.K_s:
                        player1Y_change = 10
                    if event.key == pygame.K_w:
                        player1Y_change = -10
                    if event.key == pygame.K_d:
                        if fire_delay1 > (last_fire_delay1 + 20):
                            fire_bullet1(player1X, player1Y)
                            bullet_sound.play()
                            last_fire_delay1 = fire_delay1
                    if event.key == pygame.K_LEFT:
                        if fire_delay2 > (last_fire_delay2 + 20):
                            fire_bullet2(player2X, player2Y)
                            bullet_sound.play()
                            last_fire_delay2 = fire_delay2
                    if event.key == pygame.K_ESCAPE:
                        if not game_state:
                            running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player2Y_change = 0
                    if event.key == pygame.K_UP:
                        player2Y_change = 0
                    if event.key == pygame.K_s:
                        player1Y_change = 0
                    if event.key == pygame.K_w:
                        player1Y_change = 0

            if game_state:
                fire_delay1 += 1
                fire_delay2 += 1

            player1Y += player1Y_change
            player2Y += player2Y_change
            if player1Y < 60:
                player1Y = 60
            elif player1Y > 536:
                player1Y = 536
            if player2Y < 60:
                player2Y = 60
            elif player2Y > 536:
                player2Y = 536
            player1Rect = pygame.Rect(player1X, player1Y, 64, 64)
            player2Rect = pygame.Rect(player2X, player2Y, 64, 64)

            l1 = len(bullet1X)
            i1 = 0
            while i1 < l1:
                bullet1(bullet1X[i1], bullet1Y[i1])
                bullet1X[i1] += bullet1X_change
                bullet1Rect[i1] = pygame.Rect(bullet1X[i1], bullet1Y[i1], 16, 16)
                if player2Rect.colliderect(bullet1Rect[i1]):
                    player2Health -= 8

                    bullet1X.pop(i1)
                    bullet1Y.pop(i1)
                    bullet1Rect.pop(i1)
                    l1 -= 1

                    collision_sound.play()
                i1 += 1

            if len(bullet1X) > 0:
                if bullet1X[0] > 800:
                    bullet1X.pop(0)
                    bullet1Y.pop(0)
                    bullet1Rect.pop(0)

            l2 = len(bullet2X)
            i2 = 0
            while i2 < l2:
                bullet2(bullet2X[i2], bullet2Y[i2])
                bullet2X[i2] -= bullet2X_change
                bullet2Rect[i2] = pygame.Rect(bullet2X[i2], bullet2Y[i2], 16, 16)
                if player1Rect.colliderect(bullet2Rect[i2]):
                    player1Health -= 8

                    bullet2X.pop(i2)
                    bullet2Y.pop(i2)
                    bullet2Rect.pop(i2)
                    l2 -= 1

                    collision_sound.play()
                i2 += 1

            if len(bullet2X) > 0:
                if bullet2X[0] < -16:
                    bullet2X.pop(0)
                    bullet2Y.pop(0)
                    bullet2Rect.pop(0)

            pygame.draw.rect(screen, red, (player1X + 17, player1Y - 10, 40, 5))
            pygame.draw.rect(screen, red, (player2X + 7, player2Y - 10, 40, 5))
            pygame.draw.rect(screen, green, (player1X + 17, player1Y - 10, player1Health, 5))
            pygame.draw.rect(screen, green, (player2X + 7, player2Y - 10, player2Health, 5))

            player(player1X, player1Y, player1Img)
            player(player2X, player2Y, player2Img)

            if game_state:
                if player1Health < 1:
                    winner_name = player2Name
                    game_state = False
                    fire_delay1 = last_fire_delay1
                    fire_delay2 = last_fire_delay2
                elif player2Health < 1:
                    winner_name = player1Name
                    game_state = False
                    fire_delay1 = last_fire_delay1
                    fire_delay2 = last_fire_delay2

            if not game_state:
                winner(winner_name)

            screen.blit(top_rect, center_top_text)

            pygame.display.update()

            clock.tick(60)

    def save_input():
        global name1, name2
        name1 = name1_input.get()
        name2 = name2_input.get()
          
        display_name_label = Label(user, text="Welcome {} and {}! Click below to start playing.".format(name1, name2), font=("Arial", 15))
        display_name_label.pack(pady=20)


        def play_command():
            user.destroy()
            pvp_game(name1, name2)

        
        button_play = Button(user, text="Play Now!", font=("Arial", 25), width = 20, command=play_command)
        button_play.pack(pady=10)

        controls_label = Label(user, text="Controls:\nUser 1: W/S to move up and down, D to shoot.\nUser 2: ↕ (Arrow keys) to move up and down, ← to shoot.", font=("Arial", 15))
        controls_label.pack()
        
    
    save_button = Button(user, text="Save", font=("Arial", 15), command=save_input)
    save_button.pack(pady=15)

def leaderboard_window():
    scores = Tk()
    scores.title("Highscores")

    #centering
    scores.update_idletasks()
    width = 750
    height = 600
    x = (scores.winfo_screenwidth() // 2) - (width // 2)
    y = (scores.winfo_screenheight() // 2) - (height // 2)
    scores.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    scores.resizable(0,0)

    #displaying the highscores:
    file = open("scores.csv", "r")
    reader = csv.reader(file)
    
    rows = []

    for row in reader:
        if len(row)==2:
            rows.append(row)

    headingLabel = Label(scores, text="Top 10 Highscores displayed as Username with Score:", font = ("Arial", 15))
    headingLabel.pack(pady=15)

    i = 0
    sorted_reader = sorted(rows, key=lambda x: int(x[1]), reverse=True)

    for row in sorted_reader:
        i += 1
        
        displayLabel = Label(scores, text=str(row[0] + " with " + str(row[1]) + " points"), font=("Calibri", 10))
        displayLabel.pack()

        if i >= 10:
            break


    # values = connection.execute('''SELECT * from HIGHSCORE LIMIT 0,10''')
    # i = 0 # 
    # for score in values: 
    #     for j in range(len(score)):
    #         e = Entry(scores, width=10, fg='blue') 
    #         e.grid(row=i, column=j) 
    #         e.insert(END, score[j])
        # i=i+1



def PlayGame(): #Game code here
    loading_window()
    if decision == "AI":
        user_window_ai()
    else:
        user_window_pvp()


main_menu()