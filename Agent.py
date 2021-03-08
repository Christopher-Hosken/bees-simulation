import numpy as np
import random
class Agent:
    _name = ""
    _male = False
    _id = None
    _age = 0
    _spouse = None
    _parent = False
    _children = []
    _interactions = []
    _deathAge = 0
    
    def __init__(self, newID, day):
        self._name = f"Agent{day}-{newID}"
        self._id = newID
        self._age = 0
        if random.random() < 0.512:
           self._male = True

        self.setDeathAge()

    def getDeathAge(self):
        return self._deathAge

    def setDeathAge(self):
        if self._male:
            self._deathAge = 79 + random.randint(-5, 5)
        else:
            self._deathAge = 83 + random.randint(-5, 5)
        
    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def getAge(self):
        return self._age

    def isMale(self):
        return self._male

    def isMarried(self):
        if self._spouse is not None:
            return True
        else:
            return False

    def isParent(self):
        return self._parent

    def getSpouse(self):
        return self._spouse
    
    def getChildren(self):
        return self._children

    def getInteractions(self):
        return self._interactions

    def getScore(self, id):
        if len(self._interactions) > 0:
            for i in self._interactions:
                if i[0] == id:
                    return i[1]
        return None

    def setSpouse(self, spouse):
        self._spouse = spouse.getName()

    def setChild(self, name):
        self._children.append(name)
        self._parent = True

    def setID(self, id):
        self._id = id

    def age(self):
        self.think()
        self._age += 1

    def think(self):
        pass

    def interact(self, id, score):
        if len(self._interactions) > 0:
            for i in self._interactions:
                if i[0] == id:
                    i[1] =  np.clip(i[1] + score, -1, 1)
                    return
        
        self._interactions.append([id, score])

    def forgetAgents(self, deceased):
        for deadID in deceased:
            for i in self._interactions:
                if (i[0] == deadID):
                    del self._interactions[self._interactions.index(i)]
                    break

def socialize(a, b):
    id_a = a.getID()
    id_b = b.getID()

    r = random.random()
    score = (r - 0.5) * 2

    a.interact(id_b, score)
    b.interact(id_a, score)

def tryMarry(a, b):
    id_a = a.getID()
    id_b = b.getID()
    a_score = b.getScore(id_a)
    b_score = a.getScore(id_b)
    if a_score is not None and b_score is not None:
        if a.isMale() != b.isMale():
            if a_score >= 0.9 and b_score >= 0.9:
                a.setSpouse(b)
                b.setSpouse(a)
                return True
    return False

def findSpouse(agent, _agents):
    spouseName = agent.getSpouse()
    for a in _agents:
        if a.getName() == spouseName:
            return a
    return None
