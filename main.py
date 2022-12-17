from random import choice, randint
import random
import pygame
from pygame import gfxdraw
from planet import *
from ball import *
from defaults import *
import math
pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Gravity Golf")
done = False

getTicksLastFrame = pygame.time.get_ticks()

clock = pygame.time.Clock()

class FPSCounter:
    def __init__(self, surface, font, clock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(str(int(self.clock.get_fps())) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        self.fps_text = self.font.render(str('%.3f'%self.clock.get_fps()) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

green = (127, 255, 0)
font = pygame.font.Font(None, 36)
fps_counter = FPSCounter(screen, font, clock, green, (150, 10))

def generatePlanets(minimum = 3, maximum = 6):
    global planets
    planets = []
    for i in range(randint(minimum, maximum)):
        planets.append(Planet())

def createBall(ball_starting_coordinates = None, freeze_ball = False, collision_enabled = True):
    global ball
    if ball_starting_coordinates is None:
        ball_start_coordinates = [screen_size[0]/2, screen_size[1]/2]
    ball = Ball(ball_start_coordinates, freeze_ball, collision_enabled)

def drawBackground():
    screen.fill(screen_color)

def drawPlanets():
    global planets
    for planet in planets:
        if planet.was_interrupted or update_whole_scene:
            if draw_boundingboxes:
                pygame.draw.rect(screen, "#0000ff", (*planet.boundingbox_coordinates[0], *list(map(lambda a, b: b - a, *planet.boundingbox_coordinates))), 1)
            if antialising_enabled:
                gfxdraw.filled_circle(screen, int(planet.position[0]), int(planet.position[1]), planet.radius, hex2rgb(planet.color))
                gfxdraw.aacircle(screen, int(planet.position[0]), int(planet.position[1]), planet.radius, hex2rgb(planet.color))
                planet.was_interrupted = False
            else:
                pygame.draw.circle(screen, planet.color, planet.position, planet.radius)
                planet.was_interrupted = False

def drawBall():
    if draw_boundingboxes:
        pygame.draw.rect(screen, "#0000ff", (*ball.boundingbox_coordinates[0], *list(map(lambda a, b: b - a, *ball.boundingbox_coordinates))))
    if antialising_enabled:
        gfxdraw.filled_circle(screen, int(ball.position[0]), int(ball.position[1]), ball.radius, hex2rgb(ball.color))
        gfxdraw.aacircle(screen, int(ball.position[0]), int(ball.position[1]), ball.radius, hex2rgb(ball.color))
        return pygame.Rect(ball.position[0] - ball.radius - 2, ball.position[1] - ball.radius - 2, ball.radius * 2 + 4, ball.radius * 2 + 4)
    else:
        return pygame.draw.circle(screen, ball.color, ball.position, ball.radius)

def drawLine():
    mouse_position = pygame.mouse.get_pos()
    if antialising_enabled:
        gfxdraw.aapolygon(screen, [drawline_start_coordinates, mouse_position, mouse_position], hex2rgb("#ffffff"))
        left = min(drawline_start_coordinates[0], mouse_position[0]) - 2
        top = min(drawline_start_coordinates[1], mouse_position[1]) - 2
        width = max(drawline_start_coordinates[0], mouse_position[0]) - left + 4
        height = max(drawline_start_coordinates[1], mouse_position[1]) - top + 4
        return pygame.Rect(left, top, width, height)
    else:
        return pygame.draw.line(screen, "#ffffff", drawline_start_coordinates, mouse_position)

def drawScreen():
    # global lineQueue
    global toBeUpdatedNext
    toBeUpdatedNext = []
    drawBackground()
    drawPlanets()
    toBeUpdatedNext.append(drawBall())
    
    if drawline_start_coordinates is not None:
        toBeUpdatedNext.append(drawLine())
    if show_fps:
        toBeUpdatedNext.append(pygame.Rect(0,0,280,18))
        fps_counter.render()
        fps_counter.update()
    pass

def initScene():
    global toBeUpdated
    global lineQueue
    global mouse_movement
    # Debug Globals
    global draw_boundingboxes
    global drawline_start_coordinates
    global update_whole_scene
    global show_fps
    global collision_enabled
    global antialising_enabled
    
    # Debug Functions
    draw_boundingboxes = True
    ball_starting_coordinates = None
    update_whole_scene = True
    show_fps = True
    # random.seed(11)
    fixed_number_of_planets = True
    number_of_planets = 24
    freeze_ball = False
    collision_enabled = True
    antialising_enabled = True

    # Initialization
    drawline_start_coordinates = None
    mouse_movement = pygame.mouse.get_pos()
    lineQueue = None
    toBeUpdated = []
    generatePlanets(number_of_planets, number_of_planets) if fixed_number_of_planets else generatePlanets()
    createBall(ball_starting_coordinates, freeze_ball, collision_enabled)



initScene()
drawScreen()

pygame.display.flip()

while not done:

    # EVENTS
    
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    for event in pygame.event.get():
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                drawline_start_coordinates = np.array(pygame.mouse.get_pos())
                
            case pygame.MOUSEBUTTONUP:
                acceleration = drawline_start_coordinates - pygame.mouse.get_pos()
                ball.calculateAcceleration(acceleration)
                drawline_start_coordinates = None

            case pygame.QUIT:
                done = True
    
    # PHYSICS

    t = pygame.time.get_ticks()

    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    ball.physics(deltaTime, clock.get_fps(), planets)

    # GRAPHICS
    drawScreen()
    pygame.display.update() if update_whole_scene else pygame.display.update(toBeUpdated)
    toBeUpdated = toBeUpdatedNext
    clock.tick(0)