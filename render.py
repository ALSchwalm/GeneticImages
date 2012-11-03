import pygame,sys
import cStringIO
from growth import *
from Consts import *


def transform(old_max, old_min, new_max, new_min, value):
    oldRange = old_max - old_min
    newRange = new_max - new_min
    newValue = (((float(value) - old_min) * newRange)/oldRange) + new_min
    return abs(int(newValue))


def create_image(ga):
    f = open("temp.txt", 'w')
    image_string = ""
    ga.getPopulation().sort()
    print(ga.getPopulation()[0])
    code= ga.getPopulation()[0].getCompiledCode()
    
    true_min = 0
    X, Y, Z = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_DEPTH)
    m, n, q = eval(code)
    true_max = max(m, n, q) 
    
    for Y in range(0, IMAGE_HEIGHT):
        line_string = ""
        for X in range(0, IMAGE_WIDTH):
            for Z in range(1, IMAGE_DEPTH):
                r_value, g_value, b_value = eval(code)
                line_string += " ".join([str(transform(true_min, true_max, 0, 255, abs(int(x)))) for x in [r_value, g_value, b_value]]) + " " # transform(true_min, true_max, 0, 255, abs(int(x)))   )
        image_string += line_string +"\n"
    print("Done")
    image_string = "P3\n"+str(IMAGE_WIDTH) + " " + str(IMAGE_HEIGHT) + "\n255\n" + image_string
    image_fstr = cStringIO.StringIO(image_string)
    f.write(image_string)
    return pygame.image.load(image_fstr)


def input(events):
    global image
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ga.evolve(freq_stats=5)
                image = create_image(ga)

def draw(image):
    global Surface
    global clock
    Surface.blit(image, (0, 0))

    pygame.display.flip()
    clock.tick(30)

def setup(growth):
    global ga
    global image
    global Surface
    global clock
    ga = growth
    
    pygame.init()
    
    Surface = pygame.display.set_mode((IMAGE_WIDTH,IMAGE_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    pygame.display.set_caption('Genetic Images v0.3')
    
    image = create_image(ga)

def start():
    global Surface
    while True:
        draw(image)
        input(pygame.event.get())