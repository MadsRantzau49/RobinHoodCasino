import random

startDiceAmount = 5
playersAmount = 6
playersList = []
lastPlayer = None

class PlayerInformation:
    def __init__(self, id, diceAmount, diceRoll):
        self.id = id
        self.diceAmount = diceAmount 
        self.diceRoll = diceRoll


def rollDices(d):
    return [random.randint(1,6) for _ in range(d)]

def startGame():
    for i in range(playersAmount):
        player = PlayerInformation(i,startDiceAmount,None)
        playersList.append(player)
    newRound(None)

def guess():
    return [input("amount: "),input("1-6 or k: ")]
          
def checkGuess():
    result = input("l=lift, c=continue: ")
    if result == "l":
        return False
    elif result == "c":
        return True
    else:
        checkGuess()

def newRound(loosingPlayer):
    for p in playersList:
        if loosingPlayer and loosingPlayer != p.id:
            p.diceAmount -= 1
        if p.diceAmount < 1:
            continue
        diceRoll = rollDices(p.diceAmount)
        p.diceRoll = diceRoll
    if not loosingPlayer:
        playRound(0,None,None)
    else:
        playRound(loosingPlayer,None,None)

def nextPlayer(player):
    for p in playersList:
        for i in range(1,playersAmount):
            if p.id == (player + i) and p.diceAmount > 0:
                return p.id
    for p in playersList:
        if p.diceAmount > 0 and p.id != player:
            return p.id
    exit()

def validGuess(guess,lastGuess):
    if guess[0] < lastGuess[0]:
        return False
    
    if guess == lastGuess:
        return False
    
    if guess[0] > lastGuess[0]:
        return True
    
    if guess[0] == lastGuess[0]:
        if lastGuess[1] == "k":
            return True
        
        if guess[1] == "k":
            return False
        
        if guess[1] < lastGuess[1]:
            return False
    return True

def checkForStair(diceRoll):
    diceRoll.sort()
    if diceRoll[0] == 1:
        for i in range(len(diceRoll)-1):
            if (diceRoll[i] + 1) != diceRoll[i+1]:
                return False
    else:
        return False
    return True

def guessIsTrue(guess,result):
    print(result)
    if guess[1] == "k":
        for r in result:
            if result[r] >= int(guess[0]):
                return True
        return False
    if int(guess[0]) <= result[int(guess[1])]:
        return True
    return False        


def checkAllDices():
    result = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for p in playersList:
        if checkForStair(p.diceRoll):
            print("TRAPPE")
            for d in result:
                result[d] += len(p.diceRoll) + 1
        else:
            for dice in p.diceRoll:
                result[dice] += 1
                if dice == 1:
                    for p in result:
                        if p != 1:
                            result[p] += 1

    return result        


def playRound(player,lastGuess,lastPlayer):
    nextPlayerId = nextPlayer(player)
    if not lastGuess:
        playerGuess = guess()
        playRound(nextPlayerId,playerGuess,player)
        
    elif checkGuess():
        playerGuess = guess()
        if validGuess(playerGuess,lastGuess):
            playRound(nextPlayerId,playerGuess,player)
        else:
            print("INVALID")
            exit()
    else:
        result = checkAllDices()
        if guessIsTrue(lastGuess,result):
            print("player ",player, "lost")
        else:
            print("player ",lastPlayer, "lost")


        


startGame()

for p in playersList:
    print(p.id,p.diceAmount,p.diceRoll)