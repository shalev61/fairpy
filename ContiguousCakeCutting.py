"""
Contiguous Cake Cutting: Hardness Results and Approximation Algorithms∗
Programmers: prof. Erel Segal-Halevi for Agent
and          Shalev Goldshtein for algor1
Since: 2020-03
"""

from abc import ABC, abstractmethod
from typing import Optional, Any

import numpy as np
from typing import *
from allocations import *
from agents import *

import logging
logger = logging.getLogger(__name__)


#import sys
#logger.addHandler(logging.StreamHandler(sys.stdout))
#logger.setLevel(logging.INFO)

# line 5. 'some agent in N values [`, 1] at least 1/3'
# agentN - indexes of all existing agents
# agentL - all agents
def hasBiggerThanThird(left, agentN, agentL):
    """
    Answer if there is part that is bigger then 1/3 till the end of the cake.

    :param left: Our Location on this moment.
    :param agentN: the number of agents.
    :param agentL: the agents themselves.
    :return: true if there is at list one the has value more then 1/3 .
    & false where there is no one that has value that is more or equal to 1/3.

    >>> c1 = PiecewiseConstantAgentNormalized([2, 8, 2])
    >>> c2 = PiecewiseConstantAgentNormalized([4, 2, 6])
    >>> lsC = [c1,c2]
    >>> hasBiggerThanThird(0.0,[0,1],lsC)
    True
    >>> hasBiggerThanThird(0.85,[0,1],lsC)
    False
    >>> hasBiggerThanThird(0.6,[1],lsC)
    True

    """
    # for every agent
    for agentIndex in agentN:
        # if the segment [left,1] is evaluated >= 1/3
        if (agentL[agentIndex].eval(left, 1.0) >= (1 / 3)):
            logger.info("There is a agent with more then 1/3 value - Therefore and accordingly we are doing another round in the loop")
            return True
    logger.info("There isn't a agent with more then 1/3 value - we are exist the loop")
    return False


# Algorithm 1 1/3-Envy-Free Algorithm
# AgentList is all agents
def algor1(AgentList):
    """
    Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value  {[(NORMALIZED)]}.

    :param start: Location on cake where the calculation starts.
    :param targetValue: required value for the piece [start,end]
    :return: the end of an interval with a value of target_value.
    If the value is too high - returns None.

    >>> aa = PiecewiseConstantAgentNormalized([2, 8, 2], name="aa")
    >>> bb = PiecewiseConstantAgentNormalized([4, 2, 6], name="bb")
    >>> lstba = [aa,bb]
    >>> algor1(lstba)
    > Agent aa gets the segment: [0.3333333333333333, 1.0]
    > Agent bb gets the segment: [0.0, 0.3333333333333333]
    <BLANKLINE>

    >>> a0 = PiecewiseConstantAgentNormalized([4, 10, 20], name="a0")
    >>> a1 = PiecewiseConstantAgentNormalized([14, 42, 9, 17], name="a1")
    >>> a2 = PiecewiseConstantAgentNormalized([30, 1, 12], name="a2")
    >>> lstaaa = [a0,a1,a2]
    >>> algor1(lstaaa)
    > Agent a0 gets the segment: [0.3824514991181658, 1.0]
    > Agent a1 gets the segment: [0.15925925925925924, 0.3824514991181658]
    > Agent a2 gets the segment: [0.0, 0.15925925925925924]
    <BLANKLINE>

    """
    l = 0.00
    lenAgents = len(AgentList)
    # N = list(range(0, lenAgents))
    N = [i for i in range(lenAgents)]


    # Mlist is the list who save the M Parts of the cake
    Mlist = [None] * lenAgents

    # the leftest point of each of the agent to fulfill the condition of the 1/3
    rList = [None] * lenAgents

    # for saving who was the last agent to remove
    lastAgentRemove = -1

    # the main loop
    while hasBiggerThanThird(l, N, AgentList):
        for i in N:
            if AgentList[i].eval(l, 1.0) >= (1 / 3):
                #where it equal 1/3
                rList[i] = (AgentList[i].mark(l, (1 / 3)))
            else:
                rList[i] = 1
        # j - agent with smallest rList value (r[i])
        j = N[0]
        # r - smallest rList value (r[i])
        r = rList[N[0]]
        # find j and r (finds minimum)
        for k in N:
            if rList[k] < r:
                j = k
                r = rList[k]
        logger.info("From The agents who remained The agent (%s) is with the leftest point - which is %s.", AgentList[j].name(),str(r))
        # gives agent j this segment , moves l to the right (r)
        Mlist[j] = [l, r]
        l = r

        # remove j
        N.remove(j)

        lastAgentRemove = j
        if len(N) == 0:
            break
    # if N is not empty
    if N:
        # arbitrary agent in N

        j = N[0]
        logger.info(" (%s) is getting the rest. %s till 1.0",AgentList[j].name(), str(l))
        Mlist[j] = [l, 1.0]
    else:
        logger.info("There is no agents that remained")
        j = lastAgentRemove
        logger.info(" we are adding to (%s) the rest. %s till 1.0", AgentList[j].name(), str(l))
        # [a, l] unite with [l, 1] => [a, 1]
        Mlist[j][1] = 1.0
    logger.info("")

    #tempprint = ""
    rStemp = reprSegement(AgentList,Mlist)
    #for i, allocation in enumerate(Mlist):
        #print("> Agent " + str(i) + " gets the segment: " + str(allocation))
        #logger.info("> Agent %s gets the segment: %s", AgentList[i].name(), str(allocation))
        #tempprint += "> Agent "+ AgentList[i].name() +" gets the segment: "+ str(allocation) + "\n"

    return rStemp


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))