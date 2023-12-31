# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        legalMoves.remove("Stop")

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = successorGameState.getFood().asList()
        foodScore = 1000000
        for food in foodList:
            if foodScore > manhattanDistance(newPos, food):
                foodScore=  manhattanDistance(newPos, food)




        # if ghost is present too close,
        # check if they are scared right now and have more scared time left.
        # if yes than go for it, else do not
        for ghost in successorGameState.getGhostStates():
            if (manhattanDistance(newPos, ghost.getPosition() ) < 5):
                if ghost.scaredTimer  > 2 * manhattanDistance(newPos, ghost.getPosition()):
                    return 1000000
                else:
                    return -1000000


        # as capsule gives more points, taking capsiule
        # distance as well. If it is too near, go for it
        for capsule in successorGameState.getCapsules():
            if (manhattanDistance(newPos, capsule ) < 1):
                return 1000000



        # reciprocal of food score as suggested in question
        return successorGameState.getScore() + 1 / foodScore



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        _, action = self.minimax(gameState, 0, 0)

        return action
    
    
    def minimax(self, state, agentIndex, depth):
        """
        Outputs the score value and action as an array. Score is required 
        to pass in  the child max and min functions whereas action is 
        required to pass to the getAction function

        """
        
        # Terminating condition
        if state.isLose() or state.isWin() or depth == self.depth * state.getNumAgents():
            return state.getScore(), ""

        # As the pacman has the index 0
        if agentIndex == 0:
            return self._maxval(state, agentIndex, depth)
        else:
            return self._minval(state, agentIndex, depth)

    def _maxval(self, state, agentIndex, depth):
     
        possibleMoves = state.getLegalActions(agentIndex)
        bestVal = -100000
        bestAction = ""

        for action in possibleMoves:
            successor = state.generateSuccessor(agentIndex, action)

            # adding 1 to agentinex for the next agent turn
            # tho modulo by number of agents
            currVal = self.minimax(successor, (depth + 1)%state.getNumAgents(), depth+1)[0]

            if currVal > bestVal:
                bestVal = currVal
                bestAction = action

        return bestVal, bestAction
    
    def _minval(self, state, agentIndex, depth):
     
        possibleMoves = state.getLegalActions(agentIndex)
        bestVal = 100000
        bestAction = ""

        for action in possibleMoves:
            successor = state.generateSuccessor(agentIndex, action)

            # adding 1 to agentinex for the next agent turn
            # tho modulo by number of agents
            currVal = self.minimax(successor, (depth + 1)%state.getNumAgents(), depth+1)[0]

            if currVal < bestVal:
                bestVal = currVal
                bestAction = action

        return bestVal, bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphabeta(gameState, 0, 0, -100000, 100000)[1]

    def alphabeta(self, state, agentIndex, depth, alpha, beta):
        if state.isLose() or state.isWin() or depth == self.depth * state.getNumAgents():
            return self.evaluationFunction(state), ""
        
        # As the pacman has the index 0
        if agentIndex == 0:
            return self._maxval(state, agentIndex, depth, alpha, beta)
        else:
            return self._minval(state, agentIndex, depth, alpha, beta)

    def _maxval(self, state, agentIndex, depth, alpha, beta):
        possibleMoves = state.getLegalActions(agentIndex)
        bestVal = -100000
        bestAction = ""

        for action in possibleMoves:
            successor = state.generateSuccessor(agentIndex, action)

            # adding 1 to agentinex for the next agent turn
            # tho modulo by number of agents
            currVal = self.alphabeta(successor, (depth + 1)%state.getNumAgents(), depth+1, alpha, beta)[0]

            if currVal > bestVal:
                bestVal = currVal
                bestAction = action
            if bestVal > beta:
                return bestVal, bestAction
            else:
                alpha = max(alpha, bestVal)

        return bestVal, bestAction

    def _minval(self, state, agentIndex, depth, alpha, beta):
        possibleMoves = state.getLegalActions(agentIndex)
        bestVal = 100000
        bestAction = ""

        for action in possibleMoves:
            successor = state.generateSuccessor(agentIndex, action)

            # adding 1 to agentinex for the next agent turn
            # tho modulo by number of agents
            currVal = self.alphabeta(successor, (depth + 1)%state.getNumAgents(), depth+1, alpha, beta)[0]

            if currVal < bestVal:
                bestVal = currVal
                bestAction = action
            if bestVal < alpha:
                return bestVal, bestAction
            else: 
                beta = min(beta, bestVal)

        return bestVal, bestAction



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        return self.expectimax(gameState, 0, self.depth * gameState.getNumAgents(), "" )[1]

    def expectimax(self, state, agentIndex, depth, action):
        if state.isLose() or state.isWin() or depth == 0:
            return self.evaluationFunction(state), ""

        # As the pacman has the index 0
        if agentIndex == 0:
            return self._maxval(state, agentIndex, depth, action)
        else:
            return self._expval(state, agentIndex, depth, action)

    def _maxval(self, state, agentIndex, depth, action):
        possibleMoves = state.getLegalActions(agentIndex)
        bestVal = -100000
        bestAction = ""


        for move in possibleMoves:
            nextIndex = (agentIndex + 1) % state.getNumAgents()
            currAction = None

            if self.depth * state.getNumAgents() != depth:
                currAction = action
            else:
                currAction = move
            currVal = self.expectimax(state.generateSuccessor(agentIndex, move), nextIndex,  depth - 1, currAction)[0]


            if currVal > bestVal:
                bestVal = currVal
                bestAction = move

        return bestVal, bestAction

    def _expval(self, state, agentIndex, depth, action):
        possibleMoves = state.getLegalActions(agentIndex)
        averageScore = 0
        prob = 1/ len(possibleMoves)
        for move in possibleMoves:
            nextIndex = (agentIndex + 1) % state.getNumAgents()
            val, act = self.expectimax(state.generateSuccessor(agentIndex, move),
                                         nextIndex, depth - 1, action)
            averageScore += val * prob
        return averageScore, action



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    pacmanPos = currentGameState.getPacmanPosition()

    foods = currentGameState.getFood().asList()

    foodScore = 1

    gameScore = currentGameState.getScore()

  
    foodDis = [manhattanDistance(pacmanPos, fpos) for fpos in foods]

    foodCount = len(foods)
    capsuleCount = len(currentGameState.getCapsules())
    if foodCount > 0:
        foodScore = min(foodDis)


    return 20/foodScore + 300*gameScore - 150*foodCount -20*capsuleCount



# Abbreviation
better = betterEvaluationFunction
