import pygame
import math
import random

# Display size parameters
screen_width = 800
screen_height = 600

# Colors
RED = (255, 0, 0)
LBLUE = (105, 105, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.display.set_caption('High Flyer')
screen = pygame.display.set_mode((screen_width, screen_height))

# Load in sound effects and music
death_sound = pygame.mixer.Sound("Sound\Explosion.wav")
button_sound = pygame.mixer.Sound("Sound\Button.wav")

# Load in visuals
background = pygame.transform.rotozoom(
    pygame.image.load("Images\Background.png"), 90, 0.2).convert_alpha()
player_img = pygame.image.load("Images\Rocket.png").convert_alpha()
obstacle_color = LBLUE

# Parameters for the game (sizes, speed, etc.)
player_speed = 7.5
player_size = [25, 50]
obstacle_size = 20
game_speed = 9.5
game_speed_increase_rate = 0.75
fps = 60


class Player:
    """A class that represents the player object."""

    def __init__(self, speed, width, height):
        """Initializes player's attributes based on input parameters"""
        self.size = [width, height]
        self.speed = speed
        self.pos = [screen_width/2, screen_height - 2 * self.size[1]]
        self.rotate_angle = 0

    def move(self):
        """Controls the player's movement from left to right, along with the rotation animation."""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.pos[0] > self.speed:
            # If left arrow key is pressed, move left and rotate left
            self.pos[0] -= self.speed
            self.rotate_angle = 90 - \
                math.degrees(math.atan(game_speed/player_speed))
        elif pressed_keys[pygame.K_RIGHT] and self.pos[0] < screen_width - self.speed:
            # If right arrow key is pressed, move right and rotate right
            self.pos[0] += self.speed
            self.rotate_angle = math.degrees(
                math.atan(game_speed/self.speed)) - 90
        else:
            # If player is moving straight, gradually reduce the rotation angle
            self.rotate_angle *= 0.5

    def detect_collision(self, obstacles_list):
        """Detects if the player collides with any of the obstacles"""
        for obstacle in obstacles_list:
            # Check for collisions with each enemy using a loop
            player_x, player_y = self.pos
            obstacle_x, obstacle_y = obstacle.pos

            if (obstacle_x >= player_x and obstacle_x <= player_x + self.size[0]) or (player_x >= obstacle_x and player_x <= obstacle_x + obstacle.size):
                if (obstacle_y >= player_y and obstacle_y <= (player_y + self.size[1])
                        ) or (player_y >= obstacle_y and player_y <= (obstacle_y + obstacle.size)):
                    return True

        return False

    def draw(self, screen):
        """Draws player on the screen, using the image and player size."""
        player_sprite = pygame.transform.rotozoom(
            player_img, self.rotate_angle, self.size[0]/player_img.get_rect().width)
        screen.blit(player_sprite, self.pos)


class Obstacle:
    """A class that represents the obstacles the player has to try to avoid."""

    def __init__(self, obstacle_size, game_speed):
        """Initializes obstacle objects."""
        self.size = obstacle_size
        self.pos = [random.randint(self.size, screen_width - 2 * self.size), 0]
        self.speed = game_speed

    def fall(self):
        """Controls animation of obstacles moving downward."""
        if self.pos[1] >= 0 and self.pos[1] < screen_height:
            self.pos[1] += self.speed
        else:
            self.pos = [random.randint(
                self.size, screen_width - 2 * self.size), 0]
            self.speed += game_speed_increase_rate

    def draw(self, screen):
        """Draws obstacle on the screen."""
        pygame.draw.rect(screen, obstacle_color,
                         (self.pos[0], self.pos[1], 20, 20))


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    """Function for wrapping text"""
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


def button(screen, x, y, width, height, color=WHITE, text='', textcolor=BLACK, fontsize=11, font='Arial', no_rect=False):
    """Function that allows you to easily create a button, or any text in general"""

    center_x, center_y = x + width/2, y + height/2

    # Draw rectangle
    if not no_rect:
        pygame.draw.rect(screen, color, (x, y, width, height))

    # Display text
    pygame.font.init()
    myfont = pygame.font.SysFont(font, fontsize)
    text = myfont.render(text, True, textcolor)
    screen.blit(text, [center_x - text.get_rect().width /
                       2, center_y - text.get_rect().height/2])

    # Actual functionality
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(mouse_x, mouse_y, x, x + width, y, y + height)
            if (mouse_x >= x and mouse_x <= x + width) and (mouse_y >= y and mouse_y <= y + height):
                button_sound.play()
                print("Working")
                return True


home_screen = True
by_pos = 0

pygame.mixer.music.load('Sound\Home_Screen_Music.mp3')
pygame.mixer.music.play(-1)

while home_screen:

    # Check to see if user presses quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            home_screen = False
            running = False

    # Scrolling background
    rel_by_pos = by_pos % background.get_rect().height
    screen.blit(background, (0, rel_by_pos - background.get_rect().height))
    if rel_by_pos < screen_height + background.get_rect().height:
        screen.blit(background, (0, rel_by_pos))
    by_pos += game_speed

    button(screen, 0, 50, screen_width, 200, color=BLACK, text='HIGH FLYER',
           textcolor=WHITE, fontsize=60, font="Courier New")

    if (button(screen, screen_width/2 - 200, 300, 400, 100, color=GREEN,
               text=f'START', textcolor=WHITE, fontsize=50, font='Courier New')):
        home_screen = False
        pygame.mixer.fadeout(10000)
        running = True
    if (button(screen, screen_width/2 - 200, 450, 400, 100, color=LBLUE,
               text=f'INSTRUCTIONS', textcolor=WHITE, fontsize=50, font='Courier New')):
        instructions_page = True
        while instructions_page:
            # Check if user presses quit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    instructions_page = False
                    home_screen = False
                    running = False

            screen.fill(LBLUE)
            drawText(screen, "Dodge the obstacles as you fly higher and higher. Use the left and right arrow keys to move horizontally. The game will get faster and faster as you progress throughout the course. Good luck!",
                     WHITE, pygame.Rect(20, 20, screen_width - 40, 450), pygame.font.SysFont('Courier New', 45))
            if (button(screen, screen_width/2 - 200, 450, 400, 100, color=ORANGE,
                       text="HOME SCREEN", textcolor=WHITE, fontsize=50, font='Courier New')):
                instructions_page = False
            pygame.display.update()

    pygame.display.update()

while running:
    # Keep on looping code until user exits out of application

    # Initializing variables for new game
    score = 0
    game_over = False

    player = Player(player_speed, player_size[0], player_size[1])
    obstacles = [Obstacle(obstacle_size, game_speed) for _ in range(10)]

    pygame.mixer.music.load('Sound\Music.mp3')
    pygame.mixer.music.play(-1)

    screen.fill(GREEN)
    button(screen, screen_width/2, screen_height/2, 0, 0, text='GO!',
           textcolor=WHITE, fontsize=120, font='Courier New')
    pygame.display.update()
    pygame.time.delay(500)

    clock = pygame.time.Clock()

    while not game_over:
        # Loop that repeats during the course of the game

        # Clock ticks at specified fps
        clock.tick(fps)

        # Increment score
        score += round(obstacles[0].speed**2 * 0.01)

        # Scrolling background
        rel_by_pos = by_pos % background.get_rect().height
        screen.blit(background, (0, rel_by_pos - background.get_rect().height))
        if rel_by_pos < screen_height + background.get_rect().height:
            screen.blit(background, (0, rel_by_pos))
        by_pos += game_speed

        # Check to see if user exits out of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                running = False

        # Update player and obstacle positions
        player.move()
        for obstacle in obstacles:
            obstacle.fall()

        # Draw player and obstacles on the screen
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Check to see if collision occurs (if it does then end the game)
        if player.detect_collision(obstacles):
            game_over = True
            death_sound.play()
            pygame.mixer.music.stop()

        # Score text display
        myfont = pygame.font.SysFont('Courier New', 30)
        textsurface = myfont.render(f'SCORE: {score}', True, WHITE)
        button(screen, 0, 0, 250, 75, color=BLACK,
               text=f'SCORE: {score}', textcolor=WHITE, fontsize=30, font='Courier New')

        pygame.display.update()

    # GAME OVER SCREEN
    stalled = True
    while stalled:
        screen.fill(BLACK)
        myfont = pygame.font.SysFont('Courier New', 60)
        textsurface = myfont.render(f'SCORE: {score}', True, WHITE)
        screen.blit(textsurface, (200, 200))
        textsurface = myfont.render('GAME OVER', True, GREEN)
        screen.blit(textsurface, (200, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                stalled = False
        # If user presses the "RETRY" button, go back to the top of the loop
        if (button(screen, 100, 400, 250, 150, GREEN, "RETRY", WHITE, 50, "Courier New")):
            running, stalled = True, False
        # If the user presses "QUIT", exit out of the game
        elif (button(screen, 450, 400, 250, 150, RED, "QUIT", WHITE, 50, "Courier New")):
            running, stalled = False, False

        pygame.display.update()

pygame.quit()
