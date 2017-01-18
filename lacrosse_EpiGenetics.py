
import random,copy
def distance(p1,p2):
    return int((((p1[0]-p2[0]) **2) + ((p1[1]-p2[1])**2))**0.5)
def prob(p):
    r = random.randint(0,99)
    if r >= p:
        return False
    return True
class Ball(object):
    """"""
    def __init__(self):
        super(Ball, self).__init__()
        self.x = 0
        self.y = 0
    def gotoPlayer(self,player):
        self.x = player.x
        self.y = player.y
class Goal(object):
    def __init__(self):
        super(Goal,self).__init__()
        self.x = 0
        self.y = 0
        self.r = 50
    def setCoords(self,x,y):
        self.x,self.y = x,y
    def ObjectinGoal(self,thing):
        if thing.x < self.x and self.y+self.r>thing.y>self.y-self.r:
            return True
        else:
            return False
class Defender(object):
    """ 3 types of defenders: mario, stationary, and polygon
    Mario goes back and forth. Stationary stays in front of the goal. Polygon goes to a series of points."""
    def __init__(self, name = "mario"):
        super(Defender, self).__init__()
        self.name = name
        self.mspeed = 5
        self.width = 5
        self.height = 5
        self.x = 0
        self.y = 0
        self.tpos = [(150,0),(100,50),(100,-50)]
        self.xtspeed = 0
        self.ytspeed = 0
        self.cur_tpos = 0
        return None
    def calc_poly_speeds(self,goal):
        tdist = distance([self.x,self.y],goal)
        xdist = self.x - goal[0]
        ydist = self.y - goal[1]
        self.xtspeed = xdist/tdist
        self.ytspeed = ydist/tdist
    def goto(self,goal):
        current_point = [self.x,self.y]
        end_point = goal

        x_distance = end_point[0]-current_point[0]
        y_distance = end_point[1]-current_point[1]

        if abs(x_distance) > abs(y_distance):
            if x_distance <= 0:
                current_point[0] -= 1
            else:
                current_point[0] += 1
                self.x = current_point[0]
                self.y = current_point[1]

        elif abs(x_distance) < abs(y_distance):
            if y_distance <= 0:
                current_point[1] -= 1
            else:
                current_point[1] += 1
                self.x = current_point[0]
                self.y = current_point[1]

        else:
            if distance(current_point,end_point) < 5:
                current_point = end_point
            else:
                current_point[1] += 2

        self.x = current_point[0]
        self.y = current_point[1]
    def changeType(self,name):
        self.name = name
    def act(self):
        if self.name not in ["mario","stationary","polygon"]:
            raise Exception("algorithm not defined: %s" % self.name)
        else:
            if self.name == "mario":
                if self.y > 50:
                    self.mspeed = -10
                if self.y < -50:
                    self.mspeed = -10
                self.y += self.mspeed
            elif self.name == "stationary":
                self.x,self.y = 150,0
            elif self.name == "polygon":
                if (self.x,self.y) in self.tpos:
                    for i in tpos:
                        if (self.x,self.y) == i:
                            self.calc_poly_speeds(i)
                self.x,self.y += self.xtspeed,self.ytspeed

goal = Goal()
goal.setCoords(300,0)
ball = Ball()
defender = Defender()
class Player(object):
    """"""
    def __init__(self,sequence=[0 for i in range(40)]):
        super(Player, self).__init__()
        self.x = 0
        self.y = 0
        self.routine = sequence
        self.doshoot = []
        self.noshoot = []
    def clone(self):
        return self
    def mate(self,parent1,parent2):

        cut1 = random.randint(0,len(parent))

        sister = copy.copy(parent1)
        sister[cut1] = copy.copy(parent2[cut1])

        brother = copy.copy(parent2)
        brother[cut1] = copy.copy(parent1[cut1])

        baby1 = copy.copy(sister)
        baby1[cut1] = copy.copy(brother[cut1])

        baby2 = copy.copy(brother)
        baby2[cut1] = copy.copy(sister[cut1])

        if len(brother) > len(sister):
            del brother[-1]
        elif len(brother) < len(sister):
            del sister[-1]
        else:
            pass
        for i in [sister,brother,baby1,baby2]:
            fakex = 0
            fakey = 0
            for j in range(len(brother)):
                if i[j] == 1:
                    fakex += 10
                elif i[j] == 2:
                    fakex -= 10
                elif i[j] == 3:
                    fakey += 10
                elif i[j] == 4:
                    fakey -= 10
                else:
                    for pos in self.noshoot:
                        if (fakex,fakey) == (pos["x"],pos["y"]) and j == pos["t"] and prob(70):
                            i[j] = random.randint(0,4)
                for pos in self.doshoot:
                    if (fakex,fakey) == (pos["x"],pos["y"]) and j == pos["t"] and prob(60):
                        i[j] = 5
        return sister, brother, baby1, baby2
    def shoot(self):
        ball.gotoPlayer(self)
        xdist = ball.x - goal.x
        ydist = ball.y - goal.y
        tdist = distance([ball.x,ball.y],[goal.x,goal.y])
        for i in range(tdist):
            ball.x += xdist/tdist
            ball.y += ydist/tdist
            if defender.x + defender.width > ball.x > defender.x - defender.width and defender.y+defender.height>ball.y>defender.y-defender.height:
                return False
        return True if goal.ObjectinGoal(ball)
    def mutate(self,individual):
        if prob(10):
            selected = random.randint(0,len(individual)-1)
            new_value = random.randint(0,5)
            individual[selected] = new_value
            return individual
        else:
            return individual
    def act(self,t,routine):
        action = routine[t]
        score_ = 0
        if action == 1:
            self.x += 10
        elif action == 2:
            self.x -= 10
        elif action == 3:
            self.y += 10
        elif action == 4:
            self.y -= 10
        else:
            score_ = self.shoot(ball)
            if score_ == True:
                self.doshoot.append({"x":self.x,"y":self.y,"t":t})
            elif score_ == False:
                self.noshoot.append({"x":self.x,"y":self.y,"t":t})
        return 1 if score_ == 1 else 0
attack = Player()
class GA(object):
    """"""
    def __init__(self,listsize = 40, popsize = 50, num_gens = 300):
        super(GA, self).__init__()
        self.popsize = popsize
        self.population = []
        self.current_generation = 0
        self.listsize = listsize
        self.num_generations = num_gens
    def randomPopulation(self):
        return [[random.randint(0,5) for i in range(self.listsize)] for i in range(self.popsize)]
    def runIndividual(self,routine):
        # setup
        player.x,player.y = 0,0
        defender.x,defender.y = 150,0
        score = 0
        for i in range(len(routine)):
            score += player.act(i,routine)
            defender.act()
        return score
    def sortByFitness(self):
        self.population.sort(key=lambda l:self.runIndividual(l))
    def crossovers(self):
        self.sortByFitness()
        best_pop = self.population[:int(len(self.population)/2)]
        bl = int(len(best_pop)/2)
        dadas = best_pop[:bl]
        mamas = best_pop[bl:]
        pairs = zip(dadas,mamas)
        new_list = [best_pop[0]]
        for i in pairs:
            sister,brother,baby,teen = player.mate(i[0],i[1])
            new_list.append(sister)
            new_list.append(brother)
            new_list.append(baby)
            new_list.append(teen)

        self.population = copy.copy(new_list)
    def mutations(self):
        for i,v in enumerate(self.population)):
            self.population[i] = player.mutate(v)
    def evolve(self):
        self.population = self.randomPopulation()
        while self.current_generation < self.num_generations:
            self.crossovers()
            self.mutations()
        self.sortByFitness()
    def getBest(self):
        self.sortByFitness()
        return self.population[0]
