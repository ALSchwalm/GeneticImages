import pygame,sys
import cStringIO
from growth import *

def create_image(ga, image_width, image_height):
    image_string = ""
    ga.getPopulation().sort()
    print(ga.getPopulation()[0])
    r_code = ga.getPopulation()[0].getCompiledCode()
    g_code = ga.getPopulation()[1].getCompiledCode()
    b_code = ga.getPopulation()[2].getCompiledCode()
    

    for Y in range(0, image_height):
        line_string = ""
        for X in range(0, image_width):
            theta = get_theta(X, Y)
            R = get_R(X, Y)
            r_value = eval(r_code)
            g_value = eval(g_code)
            b_value = eval(b_code)
            
            line_string += " ".join([str(abs(int(x))) for x in [r_value, g_value, b_value]]) + " "
        image_string += line_string +"\n"
    print("Done")
    image_string = "P3\n"+str(image_width) + " " + str(image_height) + "\n255\n" + image_string

    image_fstr = cStringIO.StringIO(image_string)
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
                image = create_image(ga, 400, 400)

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
    #Consts
    IMAGE_WIDTH = 400
    IMAGE_HEIGHT = 400
    
    Surface = pygame.display.set_mode((IMAGE_WIDTH,IMAGE_HEIGHT), 0, 32)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    pygame.display.set_caption('Genetic Images v0.1')
    
    image = create_image(ga, IMAGE_WIDTH, IMAGE_HEIGHT)

def start():
    global Surface
    while True:
        draw(image)
        input(pygame.event.get())