import random

class Agent():
    _id = None
    _age = 0
    _joy = 0.2
    _voteChance = 1
    _voted = False
    _agentRanking = []
    _lastAgentsId = []

    def __init__(self, population, id, influence):
        self._id = id
        self._agentRanking = [0.0] * population
        self._lastAgentsId = [0] * influence

    def forget(self):
        self._lastAgentsId = [0] * len(self._lastAgentsId)
        self._agentRanking = None
        self._voted = False

    def getID(self):
        return self._id

    def getAge(self):
        return self._age

    def getJoy(self):
        return self._joy

    def getVoteChance(self):
        return self._voteChance

    def getAgentRanking(self):
        return self._agentRanking

    def getLastAgents(self):
        return self._lastAgentsId

    def setAgentScore(self, idx, score):
        self._agentRanking[idx] = score
    
    def grow(self):
        self._age += 1

    def setNewIdx(self, newIdx):
        self._id = newIdx

    def setNewAgentRanking(self, newSize):
        self._agentRanking = [0.0] * newSize

    def interact(self, agent):
        agentID = agent.getID()
        success = random.random()
        self._agentRanking[agentID] = (success - 0.5) * 2
        self.influence(agent, success)

    def influence(self, agent, success):
        for lastAgentidx in self._lastAgentsId:
            view = (self._agentRanking[lastAgentidx] * success)
            agent.setAgentScore(lastAgentidx, view)

    def vote(self):
        lowestIdx = 0
        if (random.random() <= self._voteChance):
            for i in range (0, len(self._agentRanking)):
                if (self._agentRanking[i] < self._agentRanking[lowestIdx]):
                    lowestIdx = i

            self._voted = True
            return lowestIdx

        else:
            self._voted = False
            return -1

    def learn(self, outcastIdx):
        if (self._voted):
            self._joy -= (self._agentRanking[outcastIdx] * 0.3)
        
        self.capJoy()
        self._voteChance = (self._joy*0.7)
        self.grow()
        self.forget()

    def capJoy(self):
        if (self._joy < 0):
            self._joy = 0
        elif (self._joy > 1):
            self._joy = 1