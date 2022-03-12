# Welcome to The Snake : Remastered (also caled "The Python")
# The Snake : Remastered has been programmed and designed by us both.
# Have fun, and enjoy !
# Designed and created by Sam and Fabio


# ----- START -----

# --- Main modules & libraries ---
import pygame, sys, random, time
pygame.init()

# --- Global variables ---
screen_width = 720
screen_height = 720

grid_size = 30
grid_width = screen_height / grid_size
grid_height = screen_width / grid_size

move_up = (0, -1)
move_down = (0, 1)
move_left = (-1, 0)
move_right = (1, 0)

# --- Useful functions ---
random_direction = lambda: random.choice([move_up, move_down, move_left, move_right]) #Vive le lambda

def display_image_menu(image, position, screen, extension = '.png'):
    ''' :desc: Displays an image at a position
        :param: Entries : image (str), position (tuple), screen, exetension (str)
        :param: Outs : None '''
    image_to_display = pygame.image.load("Sprites\\" + image + extension)
    return screen.blit(image_to_display,position)

def display_rotated_image(image, position, screen, rotation = 0, extension = '.png'):
    ''' :desc: Displays an image at a position with a rotation
        :param: Entries : image (str), position (tuple), screen, rotation (degrees: int) exetension (str)
        :param: Outs : None '''
    image_to_display = pygame.image.load("Sprites\\" + image + extension)
    image_to_display = pygame.transform.rotate(image_to_display, rotation)
    return screen.blit(image_to_display,position)

sprite_count = 1
def animated_background_title_screen(max, screen):
    ''' :desc: Displays a frame-by-frame animation
        :param: Entries : max: nb of available frames (int), screen
        :param: Outs : None '''
    global sprite_count
    if sprite_count > max+0.1:
        sprite_count = 1
    display_image_menu('animated_background_title_screen\\' + str(int(sprite_count)), (0,0), screen, '.jpg')
    sprite_count += 0.0185

sounds_status, musics_status, music_volume = True, True, 1
def play_music(music_sound, volume = 1, playtime = -1, extension = '.mp3'):
    ''' :desc:  Plays a music
        :param: Entries : music_title (str), volume (int: 0-1), playtime (-1 = loop), extension (str)
        :param: Outs : None '''
    global musics_status, music_volume
    pygame.mixer.music.load("Musics - Sounds/" + music_sound + extension)
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(playtime)

def stop_music():
    ''' :desc: Stops the music currently playing '''
    pygame.mixer.music.stop()

def play_sound(sounds):
    ''' :desc: Plays a sound (sounds setting, not music's)
        :param: Entries : sound to play (str)
        :param: Outs : None '''
    global sounds_status
    pygame.mixer.init()
    sound_vfx = pygame.mixer.Sound("Musics - Sounds\\" + sounds + '.wav')
    sound_vfx.set_volume(0.63)
    if sounds_status is True:
        pygame.mixer.find_channel(True).play(sound_vfx)


# --- Global (snake & food) classes ---
class Snake():
    ''' :desc: The snake's class
        :param: Entries : None
        :param: Outs : Callable class '''
    def __init__(self):
        self.lenght = 1 #Starting lenght
        self.positions = [((screen_width / 2), (screen_height/2))] #Starting position #liste pour effet de bord et ordre tête-à-queue
        self.direction = random_direction() #Starting direction (randomized)
        self.color = (17, 24, 47) #Snake color
        self.score = 0 # Snake game score
        self.game_is_running = True

    def get_head_position(self):
        ''' Get the position of the head (tuple) : (x,y) '''
        return self.positions[0] # 0 = head position (in self.positions list)

    def turn(self, coordinates):
        ''' Turn the snake in a direction from coordinates '''
        # If snake's lenght is more than one, he can only move in 3 directions (not back on himself)
        if self.lenght > 1 and (coordinates[0] * -1, coordinates[1] * -1) == self.direction:
            return
        #Else : he can go all 4 directions
        else:
            self.direction = coordinates

    def is_touching_a_border(self):
        ''' Checks if the snake touches a border '''
        current_head_position = self.get_head_position()
        if current_head_position[1] > 660 or current_head_position[1] < 30:
            return True
        elif current_head_position[0] > 660 or current_head_position[0] < 30:
            return True
        else: 
            return False

    def move(self):
        ''' Make the snakes move and die if he touches himself '''
        current_head_position = self.get_head_position()
        x, y = self.direction
        # Calculate new head location's coordinates (in 0,x,width AND 1,y,height)
        new_location_of_snake_head = (((current_head_position[0] + (x*grid_size)) % screen_width), ((current_head_position[1] + (y*grid_size)) % screen_height))
        if self.is_touching_a_border() :
            self.reset()
        elif len(self.positions) > 2 and new_location_of_snake_head in self.positions[2:]:
        # Si le serpent est plus long que 2 et se touche lui-même :
            self.reset() #On recommence (perdu)
        else: #Sinon on update le snake
            self.positions.insert(0, new_location_of_snake_head) #Ajouter la nouvelle position de la tête à la liste "positions"
            if len(self.positions) > self.lenght: #Si la liste des positions est plus grande que la taille du snake
                self.positions.pop() #On pop le dernier element de sa liste des positions


    def reset(self):
        ''' Reset the game party when you lose '''
        self.lenght = 1
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random_direction()
        global global_score_save, global_best_score_save
        global_score_save = self.score
        if global_score_save > global_best_score_save:
            global_best_score_save = global_score_save
        stop_music()
        play_sound("breaking_sound")
        time.sleep(0.8)
        score_screen()
        play_sound("starting_sound")
        play_music("playing_music")
        self.score = 1

    def draw(self, surface):
        ''' Draws the snake's character '''
        if self.direction == move_down:
            display_rotated_image("head", (self.positions[0][0]-3, self.positions[0][1]), surface, 0)
        elif self.direction == move_up:
            display_rotated_image("head", (self.positions[0][0]-2, self.positions[0][1]), surface, 180)
        elif self.direction == move_right:
            display_rotated_image("head", (self.positions[0][0], self.positions[0][1]-2), surface, 90)
        elif self.direction == move_left:
            display_rotated_image("head", (self.positions[0][0], self.positions[0][1]-2), surface, 270)
        for snake_piece in self.positions[1:]:
        # For each snake piece :
            new_rectangle = pygame.Rect((snake_piece[0], snake_piece[1]), (grid_size, grid_size)) #Create a rectangle = a piece
            display_image_menu("body", (snake_piece[0], snake_piece[1]), surface, ".png")

    def handle_keys(self):
        ''' Check for pressed keys on the snake '''
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # If the app cross (top-right corner) is pressed :
                pygame.quit()
                sys.exit() # We exit the game totally
            elif event.type == pygame.KEYDOWN:
            # Elif it's a key which is pressed down :
                if event.key == pygame.K_UP: # If it's the UP key :
                    self.turn(move_up)
                elif event.key == pygame.K_DOWN: # If it's the DOWN key :
                    self.turn(move_down)
                elif event.key == pygame.K_LEFT: # If it's the LEFT key :
                    self.turn(move_left)
                elif event.key == pygame.K_RIGHT: # If it's the RIGHT key :
                    self.turn(move_right)
                elif event.key == pygame.K_ESCAPE:
                    self.game_is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True


class Food():
    ''' :desc: The food (apple) class
        :param: Entries : None
        :param: Outs : Callable class '''
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position() # Uses the the randomize_position() function which returns a random (x,y) position ON THE GRID
    
    def randomize_position(self):
        ''' Creates a random position for the food's spawn '''
        # Each time we initialize (l.86) a food, it's position is randomize on the screen (using grid size-width-height) using the random library
        self.position = (random.randint(0, grid_width-1) * (grid_size), random.randint(0, grid_height-1) * (grid_size))
        while self.position[0] > 660 or self.position[0] < 30 or self.position[1] > 660 or self.position[1] < 30:
            self.position = (random.randint(0, grid_width-1) * (grid_size), random.randint(0, grid_height-1) * (grid_size))

    def draw(self, surface):
        ''' Draws the food (apple) '''
        new_rectangle = pygame.Rect((self.position[0], self.position[1]), (grid_size, grid_size)) # Creates a food rectangle (as for the snake rect)
        display_image_menu("apple", (self.position[0], self.position[1]), surface, ".png")
        #pygame.draw.rect(surface, self.color, new_rectangle) # Draw the rectangle
        #pygame.draw.rect(surface, (93,216,228), new_rectangle, 1) # Draw the move-on rectange


# --- Main menu & game ---
pairs = [(4,3), (12,5), (20,4), (3,8), (17,7), (8,9), (22,9), (14,11), (5,15), (10,15), (16,15), (10,20), (2,23), (15,22), (20,23)]
global_score_save = 0
global_best_score_save = 0

def drawGrid(surface):
    ''' :desc: Draws the grid (cadrillage) to move on
        :param: Entries : surface : surface
        :param: Outs : None '''
    for x in range(0, int(grid_height)):
        for y in range(0, int(grid_width)):
            if x in [0, grid_height-1] or y in [0, grid_width-1]:
                rectangle_w = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                #Affiche le rectangle en couleur RGB :
                pygame.draw.rect(surface, (87,138,52), rectangle_w)
            elif (x,y) in pairs: #Sur cases aléatoires (pour effet visuel)
                rectangle_t = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                #Affiche le rectangle en couleur RGB :
                pygame.draw.rect(surface, (145,198,44), rectangle_t)
            elif (x + y) % 2 == 0: #Sur les cases (grid) paires:
                #Creation d'un rectangle à taille fixe :
                rectangle = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                #Affiche le rectangle en couleur RGB :
                pygame.draw.rect(surface, (170,215,81), rectangle)
            else : #Sur les cases (grid) impaires:
                #Creation d'un rectangle à taille fixe :
                rectangle_i = pygame.Rect((x*grid_size, y*grid_size), (grid_size, grid_size))
                #Affiche le rectangle en couleur RGB !! couleur différente:
                pygame.draw.rect(surface, (162,209,73), rectangle_i)

def game():
    ''' :desc: MAIN game function to launch a party
        :param: Entries : None
        :param: Outs : GAME '''
    
    # --- Pre-parameters ---
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32) #0 flags and 32 depth and color mod 
    stop_music()
    play_sound("starting_sound")
    play_music("playing_music")

    # --- Play ground settings
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert() #For size and colors + update frames
    drawGrid(surface) #(redirect line 53)

    # --- We create the snake and food (apple) ---
    snake = Snake()
    food = Food()
    snake.lenght = 1
    snake.score = 1

    # --- We create some fonts to use ---
    myfont = pygame.font.SysFont("Segoe UI", 20) # Create a once-time font for "score_display"
    speedFont = pygame.font.SysFont("Segoe UI", 17) # Create a once-time font for "speedFont"
    quitFont = pygame.font.SysFont("Segoe UI", 13) # Create a once-time font for "quit_game button display"

    # :GAME LOOP:
    while snake.game_is_running:
        mouse_x, mouse_y = pygame.mouse.get_pos() # Get mouse location each frame
        speed = 9*(1 + (snake.score*0.014))
        clock.tick(speed) # Frame rate : 15fps
        snake.handle_keys() # Handle events of pressed keys
        drawGrid(surface) # Well, it draws the grid
        
        snake.move()
        if snake.get_head_position() == food.position:
        # If the snakes eats a food (apple)
            snake.lenght += 1
            snake.score += 1
            food.randomize_position()
            play_sound("eat_food")
        
        esc_to_leave, colour = pygame.Rect((626, 8), (83,30)), (255,255,255) # Create a background rectangle
        if esc_to_leave.collidepoint((mouse_x, mouse_y)):
        # If we use the "QUIT" button (upper-right corner)
            colour = (200,200,200)
            if snake.click:
                play_sound("click")
                stop_music()
                snake.game_is_running = False

        # Re-draw SNAKE and FOOD :
        snake.draw(surface)
        food.draw(surface)

        # Screen frame/score update :
        screen.blit(surface, (0,0))

        # "QUIT" button display
        esc_to_leave_back = pygame.Rect((625, 7), (85,32)) # Create a background rectangle
        pygame.draw.rect(screen, (0,0,0), esc_to_leave_back) # Draw the rectangle
        pygame.draw.rect(screen, colour, esc_to_leave) # Draw the rectangle

        # "Score" section display
        score_display = quitFont.render(f"Quit game X", 1, (0,0,0))
        screen.blit(score_display, (632, 12))

        background_score = pygame.Rect((15, 4), (76,39)) # Create a background rectangle
        pygame.draw.rect(screen, (0,0,0), background_score) # Draw the rectangle

        background_score = pygame.Rect((16, 5), (74,37)) # Create a background rectangle
        pygame.draw.rect(screen, (255,255,255), background_score) # Draw the rectangle
        display_image_menu("apple", (20,7), screen, ".png")
        score_display = myfont.render(f"           {snake.score}", 1, (0,0,0))
        screen.blit(score_display, (5,10))

        # "Actual speed" display
        speed_display = speedFont.render(f"Actual speed : x{round(speed/10, 2)}", 1, (157,231,68))
        screen.blit(speed_display, (5,692))
        
        # Screen update
        pygame.display.update()


def menu():
    ''' :desc: MAIN menu function at game launch
        :param: Entries : None
        :param: Outs : MAIN MENU '''
    
    # --- Pre-parameters ---
    clock = pygame.time.Clock()
    clock.tick(30)
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32) #0 flags and 32 depth and color mod
    images = [("play_off", "play_on"), ("sounds_off", "sounds_on"), ("musics_off", "musics_on"), ("leave_off", "leave_on")]
    
    # --- Sounds and Musics ---
    global sounds_status, musics_status, music_volume
    sounds_status_image = images[1][1]
    musics_status_image = images[2][1]
    stop_music()
    play_music("menu_intro", 1, 1)
    play_music("menu_music")

    # --- Interaction loadings ---
    menu_is_running, click = True, False
    
    # :MENU LOOP:
    while menu_is_running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        animated_background_title_screen(3, screen)

        # Play button hitbox & image
        play_button = pygame.Rect(235, 441, 253, 52)
        play_button_image = images[0][0]
        # Sounds arrows hitbox
        sounds_arrow_right = pygame.Rect(238, 636 , 22, 22)
        sounds_arrow_left = pygame.Rect(155, 636 , 22, 22)
        # Musics arrows hitbox
        musics_arrow_left = pygame.Rect(151+293, 636 , 22, 22)
        musics_arrow_right = pygame.Rect(240+278, 636 , 22, 22)
        # Leave button
        leave_button = pygame.Rect(564, 680, 145, 35)
        leave_button_image = images[3][0]

        # --- Buttons colliders ---
        if play_button.collidepoint((mouse_x, mouse_y)):
            play_button_image = images[0][1]
            if click:
                game()
                play_music("menu_intro", 1, 1)
                play_music("menu_music")
        if leave_button.collidepoint((mouse_x, mouse_y)):
            leave_button_image = images[3][1]
            if click:
                play_sound("click")
                pygame.quit()
                sys.exit() # We exit the game totally
        if sounds_arrow_left.collidepoint((mouse_x, mouse_y)):
            if click:
                play_sound("click")
                if sounds_status is True:
                    sounds_status, sounds_status_image = False, images[1][0]
                else:
                    sounds_status, sounds_status_image = True, images[1][1]
        if sounds_arrow_right.collidepoint((mouse_x, mouse_y)):
            if click:
                play_sound("click")
                if sounds_status is True:
                    sounds_status, sounds_status_image = False, images[1][0]
                else:
                    sounds_status, sounds_status_image = True, images[1][1]
        if musics_arrow_left.collidepoint((mouse_x, mouse_y)):
            if click:
                play_sound("click")
                if musics_status is True:
                    musics_status, musics_status_image = False, images[2][0]
                    pygame.mixer.music.set_volume(0)
                    music_volume = 0
                else:
                    musics_status, musics_status_image = True, images[2][1]
                    pygame.mixer.music.set_volume(1)
                    music_volume = 1
        if musics_arrow_right.collidepoint((mouse_x, mouse_y)):
            if click:
                play_sound("click")
                if musics_status is True:
                    musics_status, musics_status_image = False, images[2][0]
                    pygame.mixer.music.set_volume(0)
                    music_volume = 0
                else:
                    musics_status, musics_status_image = True, images[2][1]
                    pygame.mixer.music.set_volume(1)
                    music_volume = 1
        
        # --- Button displays ---
        if sounds_status : sounds_status_image = "sounds_on"
        else : sounds_status_image = "sounds_off"
        if musics_status : musics_status_image = "musics_on"
        else : musics_status_image = "musics_off"
        display_image_menu(play_button_image, (227,433), screen, ".png")
        display_image_menu(sounds_status_image, (161,635), screen, ".png")
        display_image_menu(musics_status_image, (448,635), screen, ".png")
        display_image_menu(leave_button_image, (560,675), screen, ".png")

        display_image_menu("scores", (5,6), screen, ".png")

        # --- Fonts creation & displays ---
        myfont = pygame.font.SysFont("Segoe UI", 68) # Create a once-time font for "score_display"
        myfont2 = pygame.font.SysFont("Segoe UI", 55) # Create a once-time font for "score_display"
        best_score_display = myfont.render(f"{str(global_best_score_save).zfill(2)}", 1, (245,65,73))
        screen.blit(best_score_display, (40,12))
        last_score_display = myfont2.render(f"{str(global_score_save).zfill(2)}", 1, (216,143,52))
        screen.blit(last_score_display, (615,25))

        # --- Events handler ---
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.K_LALT and event.type == pygame.K_F4:
                pygame.quit()
                sys.exit()

        # --- Display updates ---
        pygame.display.set_caption("The Snake : NSI Remastered")
        pygame.display.update()
    

def score_screen():
    ''' :desc: SCORE screen function at the end of the game
        :param: Entries : None
        :param: Outs : SCORE SCREEN '''

    # --- Pre-parameters ---
    clock = pygame.time.Clock()
    clock.tick(20)
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32) #0 flags and 32 depth and color mod
    scoreFont = pygame.font.SysFont("Segoe UI", 75) # Create a once-time font for "score_display"

    # --- Interaction loadings ---
    images = [("quit_off", "quit_on"), ("start_off", "start_on")]
    menu_is_running, click = True, False
    stop_music()
    play_music("score_music", 0.3, 1)
    
    # :SCREEN LOOP:
    while menu_is_running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        display_image_menu("score_screen", (0,0), screen, ".jpg")

        # Play button hitbox & image
        play_button = pygame.Rect(257, 592, 207, 50)
        play_button_image = images[1][0]
        # Sounds arrows hitbox
        quit_button = pygame.Rect(583, 44, 97, 28)
        quit_button_image = images[0][0]

        # --- Buttons colliders ---
        if play_button.collidepoint((mouse_x, mouse_y)):
            play_button_image = images[1][1]
            if click:
                play_sound("click")
                menu_is_running = False
                time.sleep(1)
        if quit_button.collidepoint((mouse_x, mouse_y)):
            quit_button_image = images[0][1]
            if click:
                play_sound("click")
                menu()

        # --- Buttons displays ---
        display_image_menu(play_button_image, (240, 565), screen, ".png")
        display_image_menu(quit_button_image, (583, 44), screen, ".png")
        global global_score_save
        score_display = scoreFont.render(f"{str(global_score_save).zfill(2)}", 1, (214,63,46))
        screen.blit(score_display, (407,405))

        # --- Events handler ---
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.K_LALT and event.type == pygame.K_F4:
                pygame.quit()
                sys.exit()
        
        # --- Display updates ---
        pygame.display.set_caption("The Snake : NSI Remastered")
        pygame.display.update()


# /!\ IMPORTANT /!\
# --- Game lauching function(s) ---
menu()

