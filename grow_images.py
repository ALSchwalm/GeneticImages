import pygame, sys
import cStringIO
from pygame.locals import *
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from math import *
from random import *

pygame.init()

#Consts
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400

Surface = pygame.display.set_mode((IMAGE_WIDTH,IMAGE_HEIGHT), 0, 32)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
pygame.display.set_caption('Genetic Images v0.1')

# The operators available to the GP
@GTree.gpdec(representation="+", color="coral")
def gp_add(a, b): return a+b

@GTree.gpdec(representation="avg", color="deepskyblue")
def gp_avg(a, b): return (a+b)/2.0

@GTree.gpdec(representation="/", color="green")
def gp_divide(a, b):
	if b == 0: return 0
	else: return (a/b)

@GTree.gpdec(representation="max", color="lawngreen")
def gp_max(a, b): return max(a,b)

@GTree.gpdec(representation="min", color="lawngreen")
def gp_min(a, b): return min(a,b)

@GTree.gpdec(representation="if <", color="yellow")
def gp_iflt(a, b, c, d):
	if a<b:
		return c
	else:
		return d
		
def gp_ifgt(a, b, c, d):
	if a>b:
		return c
	else:
		return d
		
def get_theta(x, y, normal=IMAGE_WIDTH):
	x -= IMAGE_WIDTH/2
	y -= IMAGE_HEIGHT/2
	if x != 0:
		return atan(float(y)/x) * normal
	else:
		return atan(float(y)) * normal

def get_R(x_1, y_1):
	x_2 = IMAGE_WIDTH/2
	y_2 = IMAGE_HEIGHT/2
	
	c = (x_1 - x_2)**2 + (y_1 - y_2)**2
	return sqrt(c)
	
		
def transform(old_max, old_min, new_max, new_min, value):
	oldRange = old_max - old_min
	newRange = new_max - new_min
	newValue = (((float(value) - old_min) * newRange)/oldRange) + new_min
	return newValue
	
def create_image(ga, image_width, image_height):
	image_string = ""
	pop = ga.getPopulation().sort()
	r_code = ga.getPopulation()[0].getCompiledCode()
	g_code = ga.getPopulation()[1].getCompiledCode()
	b_code = ga.getPopulation()[2].getCompiledCode()
	
	max_value = 0

	for Y in range(0, image_height):
		line_string = ""
		for X in range(0, image_width):
			theta = get_theta(X, Y)
			R = get_R(X, Y)
			r_value = eval(r_code)
			g_value = eval(g_code)
			b_value = eval(b_code)
			
			if max((r_value, g_value, b_value)) > max_value:
				max_value = max((r_value, g_value, b_value))
				
			line_string += " ".join([str(abs(int(x))) for x in [r_value, g_value, b_value]]) + " "
		image_string += line_string +"\n"

	image_string = "P3\n"+str(image_width) + " " + str(image_height) + "\n255\n" + image_string
	
	image_fstr = cStringIO.StringIO(image_string)
	return pygame.image.load(image_fstr)
	

def draw(image):

	Surface.blit(image, (0, 0))

	pygame.display.flip()
	clock.tick(30)
	
def input(events):
	global image
	
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				ga.evolve(freq_stats=5)
				image = create_image(ga, 400, 400)

#Fitness function tries to reduce
#uniform results
test_list = [0] * 50
def eval_func(genome):
	code_comp = genome.getCompiledCode()
	for place in range(50):
		X = randint(0, IMAGE_WIDTH)
		Y = randint(0, IMAGE_HEIGHT)
		theta = get_theta(X, Y)
		R = get_R(X, Y)
		test_list[place] = int(eval(code_comp))
	set_len = len(list(set(test_list)))
	if set_len == 1:
		return 1
	else: 
		return random()
	  
genome = GTree.GTreeGP()
genome.setParams(max_depth=10, bestrawscore=0.00, rounddecimal=2)
genome.evaluator.set(eval_func)

ga = GSimpleGA.GSimpleGA(genome)

#Gene pool contains X, Y, constants and functions
ga.setParams(gp_terminals = ['X', 'Y', 'theta', 'R', 'ephemeral:random.uniform(-300,300)'], gp_function_prefix = "gp")

ga.setMinimax(Consts.minimaxType["minimize"])
ga.setGenerations(100)
ga.setCrossoverRate(0.5)
ga.setMutationRate(0.75)
ga.setPopulationSize(20)
ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
ga.evolve(freq_stats=5)

#print ga.bestIndividual().getParam("Expression")
image = create_image(ga, 400, 400)
def main():
	while True:
		draw(image)
		input(pygame.event.get())
	
main()