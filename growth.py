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
        
def gp_theta(p1, p2):
    x = p1[0]
    y = p2[1]
    x -= IMAGE_WIDTH/2
    y -= IMAGE_HEIGHT/2
    if x != 0:
        return [atan(float(y)/x) * IMAGE_WIDTH] * 3
    else:
        return [atan(float(y)) * IMAGE_WIDTH] * 3

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
    value = 1 - (set_len / len(test_list)) 
    
    grad_points = [ (0, 0, IMAGE_DEPTH),
                    (0, IMAGE_HEIGHT, IMAGE_DEPTH),
                    (IMAGE_WIDTH, 0, IMAGE_DEPTH),
                    (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_DEPTH)]
    
    for point1 in grad_points:
        for point2 in grad_points:
            X = abs(point1[0] - point2[0])
            Y = abs(point1[1] - point2[1])
            Z = abs(point1[2] - point2[2])
            if point1 != point2 and all(eval(code_comp)) > 200:
                value += 1
                break
    return value

def setup():
    genome = GTree.GTreeGP()
    genome.processNodes()
    
    genome.setParams(max_depth=5,
                     bestrawscore=0,
                     rounddecimal=2,
                     rangemin=0,
                     rangemax=10,
                     method="grow")
    
    genome.evaluator.set(eval_func)
    genome.crossover.set(Crossovers.GTreeCrossoverSinglePointStrict)
    ga = GSimpleGA.GSimpleGA(genome)
    
    #Gene pool contains X, Y, constants and functions
    ga.setParams(gp_terminals = ['(X, Y, Z)',
                                 '(X, Z, Y)',
                                 '(Z, Y, X)',
                                 'ephemeral:(random.uniform(-300,300), random.uniform(-300,300), random.uniform(-300,300))'],
                 gp_function_prefix = "gp")
    
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(100)
    ga.setCrossoverRate(0.9)
    ga.setMutationRate(0.05)
    ga.setPopulationSize(120)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.evolve(freq_stats=5)
    return ga
