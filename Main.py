import random
import matplotlib.pyplot as plt
from Agent import Agent

DAYS = 1095
INTERACTIONS = 12
INFLUENCE = 5
AGENTS = 10

agent_list = [None] * AGENTS

day_list = [0]*DAYS
joy_list = [0]*DAYS
population_list = [0]*DAYS
CURRENT_DAY = 0


def main():
    global agent_list, AGENTS, CURRENT_DAY
    setupPopulation()
    joy_plot = plt.subplot(211)
    plt.ylabel('Happiness')
    plt.title("Average Population Happiness")

    population_plot = plt.subplot(212)
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title("Population")

    for d in range(0, DAYS):
        CURRENT_DAY = d
        socialise()
        outcastIdx = doVote()
        editPopulation(outcastIdx)
        day_list.append(d)
        joy_list.append(getJoy())
        population_list.append(len(agent_list))
        joy_plot.plot(day_list, joy_list)
        population_plot.plot(day_list, population_list)
        plt.pause(0.1)
    
    plt.show()

def setupPopulation():
    for i in range(0, len(agent_list)):
        tmp = Agent(AGENTS, i, INFLUENCE)
        agent_list[i] = tmp

def socialise():
    for thisAgent in agent_list:
        for i in range(0, INTERACTIONS):
            while True:
                idx = random.randrange(0, len(agent_list))
                thatAgent = agent_list[idx]
                if thisAgent.getID() != thatAgent.getID():
                    break
            thisAgent.interact(thatAgent)
            thatAgent.interact(thisAgent)


def doVote():
    outcastIdx = 0
    ranking = [0] * len(agent_list)
    for agent in agent_list:
        vote = agent.vote()
        if vote != -1:
            ranking[vote] -= 1

    for i in range(0, len(ranking)):
        if (ranking[i] < ranking[outcastIdx]):
            outcastIdx = i

    return outcastIdx


def editPopulation(outcastIdx):
    global AGENTS
    del agent_list[outcastIdx]
    old = []
    for i in range (0, len(agent_list)):
        if agent_list[i].getAge() > (80 + (((random.random() - 0.5) * 2) * 25)):
            old.append(i)
    for x in old:
        del agent_list[x]

    for a in range(0, len(agent_list)):
        agent = agent_list[a]
        agent.learn(outcastIdx)
        agent.setNewIdx(a)

    repopulate()
    AGENTS = len(agent_list)

def repopulate():
    global AGENTS, CURRENT_DAY, INFLUENCE
    children = 0

    for agent in agent_list:
        if agent.getAge() > 18:
                if agent.getJoy() > 0.8:
                    if (random.random() < 0.2):
                        children += 1
    
    AGENTS += children

    for c in range(len(agent_list), AGENTS):
        child = Agent(AGENTS, c, INFLUENCE)
        agent_list.append(child)
    
    for agent in agent_list:
        agent.setNewAgentRanking(len(agent_list))


def getJoy():
    joy = 0
    for agent in agent_list:
        joy += agent.getJoy()

    joy /= len(agent_list)

    return joy

main()