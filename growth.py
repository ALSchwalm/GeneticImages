from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
from pyevolve import Crossovers
from random import *
from math import *
from Consts import *

# The operators available to the GP
@GTree.gpdec(representation="+", color="coral")
def gp_add(a, b): 
    out = [a[x] + b[x] for x in range(len(a))]
    return out

@GTree.gpdec(representation="avg", color="deepskyblue")
def gp_avg(a, b): 
    return gp_divide(gp_add(a, b), (2, 2, 2))

@GTree.gpdec(representation="/", color="green")
def gp_divide(a, b):
    if any([x == 0 for x in b]):
        return a
    else:
        return [a[x]/b[x] for x in range(len(a))]
        
    
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
        
def theta(x, y, normal=IMAGE_WIDTH):
    x -= IMAGE_WIDTH/2
    y -= IMAGE_HEIGHT/2
    if x != 0:
        return (0, 0, 0) #atan(float(y)/x) * normal
    else:
        return (1, 1, 1) #atan(float(y)) * normal

def gp_R(point):
    
    x1 = point[0]
    y1 = point[1]
    z1 = point[2]
    
    c = sqrt(((IMAGE_WIDTH/2) - x1)**2 +  ((IMAGE_HEIGHT/2) - y1)**2 + ((IMAGE_DEPTH/2) - z1)**2)
    
    return [c,c,c]

#Fitness function tries to reduce
#uniform results
def eval_func(genome):
    test_list = [0] * 200
    code_comp = genome.getCompiledCode()
    
    for place in range(len(test_list)):
        X = randint(0, IMAGE_WIDTH)
        Y = randint(0, IMAGE_HEIGHT)
        Z = randint(0, IMAGE_DEPTH)
        test_list[place] = tuple(eval(code_comp))
    set_len = len(list(set(test_list)))

    if set_len == 1:
        return 1
    elif set_len == len(test_list):
        return 0
    else: 
        return random()

def setup():
    
    genome = GTree.GTreeGP()
    genome.processNodes()
    
    genome.setParams(max_depth=5, bestrawscore=0, rounddecimal=2, rangemin=0, rangemax=10, method="grow")
    genome.evaluator.set(eval_func)
    genome.crossover.set(Crossovers.GTreeCrossoverSinglePointStrict)
    ga = GSimpleGA.GSimpleGA(genome)
    
    #Gene pool contains X, Y, constants and functions
    ga.setParams(gp_terminals = ['(X, Y, Z)', '(X, Z, Y)', '(Z, Y, X)', 'ephemeral:(random.uniform(-300,300),random.uniform(-300,300),random.uniform(-300,300))'], gp_function_prefix = "gp") #'ephemeral:random.uniform(-300,300)'
    
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(100)
    ga.setCrossoverRate(0.5)
    ga.setMutationRate(0.75)
    ga.setPopulationSize(20)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.evolve(freq_stats=5)
    return ga