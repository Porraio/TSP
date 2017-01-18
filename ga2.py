
from math import sqrt as sqrt
from random import randrange as r
from copy import deepcopy as d
from random import choice as c
import random
if not "xrange" in globals():
    # Python 3
    xrange = range
    py_version = 3
else:
    # Python 2
    py_version = 2

def prob(probability):
    if r(0,100) < probability*100:
        return True
    else:
        return False


class Individual(object):
    """docstring for Individual."""
    def __init__(self,attrs,attrrange=-1):
        super(Individual, self).__init__()
        self.fitness = 0
        self.attrs = attrs
        self.num_attrs = len(attrs)
        self.attrrange = 10 if attrrange == -1 else attrrange
    def calcFitness(self,eval_func):
        return eval_func(self)
    def crossover1point(self,other_parent):
        """ The crossover of 1D Binary String, Single Point

        .. warning:: You can't use this crossover method for binary strings with length of 1.

        """
        sister = None
        brother = None
        gMom = self.attrs
        gDad = other_parent.attrs

        if len(gMom) == 1:
            raise TypeError("The binary string is 1 unit long. Cannot do crossover.")

        cut = random.randint(1, len(gMom)-1)

        sister = d(gMom)
        sister[cut:] = gDad[cut:]

        brother = d(gDad)
        brother[cut:] = gMom[cut:]

        return (Individual(sister), Individual(brother))
    def crossover2point(self,other_parent):
        """ Takes some attrs from the mom into the dad to make the brother, and vice versa for the sister
        """
        sister = None
        brother = None
        gMom = self.attrs
        gDad = other_parent.attrs
        if len(gMom) == 1:
            raise TypeError("The Binary String have one element, can't use the Two Point Crossover method !")

        tcuts = [random.randint(1, len(gMom)-1), random.randint(1, len(gMom)-1)]

        if tcuts[0] > tcuts[1]:
            cuts = [tcuts[1],tcuts[0]]
        else:
            cuts = [tcuts[0],tcuts[1]]


        sister = d(gMom)
        sister[cuts[0]:cuts[1]] = gDad[cuts[0]:cuts[1]]

        brother = d(gDad)
        brother[cuts[0]:cuts[1]] = gMom[cuts[0]:cuts[1]]

        b = Individual(brother)
        s = Individual(sister)

        return (b,s)
    def mutate(self):
        selected_attr = c(self.attrs)
        selected_attr_copy = d(selected_attr)
        change = round(r(int(selected_attr/2),int((self.attrrange - selected_attr)/2)))
        selected_attr += c([-1,1]) * change
        i = self.attrs.index(selected_attr_copy)
        self.attrs[i] = selected_attr

class SimpleGA(object):
    """This is a fairly simple genetic algorithm coded by Chace Caven.
One example of how to use this is like this:
ga = SimpleGA()
ga.setEvaluator(eval_func)
ga.evolve()

YOU MUST SET THE EVALUATOR BEFORE EVOLVING - everything else has a default.
        """
    def __init__(self):
        super(SimpleGA, self).__init__()
        self.current_generation = 0
        self.num_generations = 300
        self.health = 0
        self.maxFitness = 0
        self.attrrange = 5
        self.num_attrs = 10
        self.mutation_rate = 0.03
        self.crossover_rate = 1.0
        self.eval_func = None
        self.population_size = 100
        self.population = []
        self.best_individual = None
        self.freq_stats = 1
    def setFrequencyStats(self,freq_stats):
        self.freq_stats = freq_stats
    def setGenerations(self,generations):
        self.num_generations = generations
    def setIndividualListRange(self,_range_):
        self.attrrange = _range_
    def setPopulationSize(self,population_size):
        self.population_size = population_size
    def setMutationRate(self,mutation_rate):
        self.mutation_rate = mutation_rate
    def setEvaluator(self,eval_func):
        self.eval_func = eval_func
    def setCrossoverRate(self,crossover_rate):
        self.crossover_rate = crossover_rate
    def random_individual(self):
        return Individual([r(0,self.attrrange) for i in xrange(self.num_attrs)],self.attrrange)
    def random_population(self):
        return [self.random_individual() for i in xrange(self.population_size)]
    def sort_pop_by_fitness(self):
        self.population.sort(reverse=True ,key=lambda individual: individual.calcFitness(self.eval_func))
    def bestIndividual(self):
        self.sort_pop_by_fitness()
        return self.population[0]
    def crossovers_mutations(self):
        size = int(len(self.population)/2)
        best_individuals = d(self.population[:size])
        best_i = best_individuals[0]
        best_len = len(best_individuals)
        dadas = best_individuals[:int(best_len/2)]
        mamas = best_individuals[int(best_len/2):]
        while len(dadas) != len(mamas):
            if len(dadas) > len(mamas):
                del dadas[-1]
            elif len(mamas) > len(dadas):
                del mamas[-1]
            else:
                break
        new_list = [best_i] + dadas + mamas
        for i in range(len(dadas)):
            if prob(self.crossover_rate):
                (sister,brother) = dadas[i].crossover1point(mamas[i])
                new_list.append(sister)
                new_list.append(brother)
        for i in range(len(new_list)):
            if prob(self.mutation_rate):
                new_list[i].mutate()
        self.population = new_list
    def evolve(self):
        self.population = self.random_population()
        while self.current_generation < self.num_generations:
            self.sort_pop_by_fitness()
            self.crossovers_mutations()
            if self.current_generation % self.freq_stats == 0:
                print("""Generation %d, Score: %d, Best Individual: %s
                    """
                % (self.current_generation,
                    self.eval_func(self.bestIndividual()),
                    self.bestIndividual().attrs))
            self.current_generation+=1
def eval_func(individual):
    score = 0
    score += sum(individual.attrs)
    for i in individual.attrs:
        if i == 0:
            score += 100
    if individual.attrs[0] == 4:
        score**=2
    if individual.attrs[2] == 3:
        score *=2

    return score
ga = SimpleGA()
ga.setEvaluator(eval_func)
ga.evolve()
