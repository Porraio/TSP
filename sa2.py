import math
import random
import copy

class SimpleSA(object):
    """docstring for SimpleSA."""
    def __init__(self, listsize, listrange, alpha=-1, stopping_T=-1):
        super(SimpleSA, self).__init__()
        self.listsize = listsize
        self.T = 150
        self.stopping_T = 0.001
        self.listrange = listrange
        self.alpha = 0.99 if alpha==-1 else alpha
        self.evaluator = None
        self.cur_solution = self.initialSolution()
        self.best_solution = self.cur_solution
        self.fitness_list = []
    def initialSolution(self):
        def r(min_num,max_num):
            return random.randrange(min_num,max_num)
        return [r(0,self.listrange) for i in range(self.listsize)]
    def setEvalulator(self,eval_func):
        self.evaluator = eval_func
    def accept(self,candidate):
        x = self.evaluator(self.cur_solution)
        x1 = self.evaluator(candidate)

        d = x-x1
        if d<=0:
            self.cur_solution = candidate
            self.cur_fitness = x1
            if self.evaluator(self.best_solution) < x1:
                self.best_solution = candidate
                self.best_fitness = x1
        else:
            prob = math.exp(d/self.T)
            if random.random() < prob:
                self.cur_solution = candidate
                self.cur_fitness = x1
    def manipulate(self,candidate):
        for j in range(self.listsize):
            candidate[j]+=random.random()*random.randrange(0,int(self.listrange/3))
    def Anneal(self):
        while self.T >= self.stopping_T:
            candidate = copy.copy(self.cur_solution)
            self.manipulate(candidate)
            l = len(candidate)/2
            i = random.randrange(0,l/2)
            candidate[i:i+l] = list(reversed(candidate[i:i+l]))
            self.accept(candidate)
            self.T *= self.alpha

            self.fitness_list.append(self.cur_fitness)
    def getBestSolution(self):
        return [self.best_solution, self.evaluator(self.best_solution)]
