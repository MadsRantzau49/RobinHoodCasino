import random
import tkinter as tk
from tkinter import simpledialog, messagebox

startDiceAmount = 4
playersAmount = 3
playersList = []
lastPlayer = None
guessAmount = None
guessValue = None
decision = None
frames = []

playerTurnLabel = None
diceResult = None
lastGuessLabel = None

# ----------------------------------------------------------------------------------------------------Setup

class PlayerInformation:
    def __init__(self, id, diceAmount, diceRoll):
        self.id = id
        self.diceAmount = diceAmount 
        self.diceRoll = diceRoll

def startGame():
    global playersList
    playersList = [PlayerInformation(i, startDiceAmount, None) for i in range(playersAmount)]
    generate_guess_layout()
    checkGuessLayout()
    newRound(None)

def toggle_frame():
    global frames
    for frame in frames:
        if frame.winfo_ismapped():
            frame.pack_forget()
        else:
            frame.pack()

def generate_guess_layout():
    global guessAmount, guessValue
    global frames
    guessAmount = tk.IntVar(value=1)  # Define guessAmount as an IntVar
    guessValue = tk.StringVar(value=1)  # Define guessValue as a StringVar
    
    tk.Button(root, text="Submit", command=lambda: (root.quit(), toggle_frame())).pack(pady=10)
    
    # Frame for the first group of radio buttons
    frame1 = tk.Frame(root)
    frame1.pack(pady=(10, 0))  # Add padding on top and no padding at bottom

    # Create and pack radio buttons for guessAmount
    amountOfDices = sum(p.diceAmount + 1 for p in playersList)
    for i in range(1, amountOfDices + 1):
        tk.Radiobutton(frame1, text=i, variable=guessAmount, value=i).pack(side=tk.LEFT, padx=5, pady=5)

    # Add an empty frame to create space
    spacer_frame = tk.Frame(root, height=20)  # Create a spacer frame with a specific height
    spacer_frame.pack()  # Pack the spacer frame to create space between groups

    # Frame for the second group of radio buttons
    frame2 = tk.Frame(root)
    frame2.pack()

    # Create and pack radio buttons for guessValue
    for i in range(1, 7):
        tk.Radiobutton(frame2, text=i, variable=guessValue, value=i).pack(side=tk.LEFT, padx=10, pady=10)

    # Additional radio button for guessValue
    tk.Radiobutton(frame2, text="kind", variable=guessValue, value="k").pack(side=tk.LEFT, padx=10, pady=10)
    frames.extend((frame1,frame2))
    
def checkGuessLayout():
    global decision
    decision = tk.BooleanVar()

    frame3 = tk.Frame(root)
    frame3.pack(pady=(10, 0))
    frames.append(frame3)
    frame3.pack_forget()

    tk.Radiobutton(frame3, text="Open", variable=decision, value=False).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Radiobutton(frame3, text="Roll", variable=decision, value=True).pack(side=tk.LEFT, padx=10, pady=10)
    
# ----------------------------------------------------------------------------------------------------Input

def find_guess():
    global guessAmount, guessValue
    root.mainloop()  # Start the mainloop to wait for user input

    selected_amount = guessAmount.get()
    selected_value = guessValue.get()

    return selected_amount, selected_value  # Return the selected values



def checkGuess():
    root.mainloop()
    selectedDecision = decision.get()
    
    return selectedDecision

# ----------------------------------------------------------------------------------------------------Rounds


def rollDices(d):
    return [random.randint(1,6) for _ in range(d)]


def newRound(loosingPlayer):
    print(loosingPlayer)
    for p in playersList:
        if (loosingPlayer or loosingPlayer == 0) and loosingPlayer != p.id:
            p.diceAmount -= 1
        if p.diceAmount < 1:
            print(p.id," har vundet")
            continue
        diceRoll = rollDices(p.diceAmount)
        p.diceRoll = diceRoll
    if not loosingPlayer:
        playRound(0, None, None)
    else:
        playRound(loosingPlayer, None, None)

def nextPlayer(player):
    for p in playersList:
        for i in range(1, playersAmount):
            if p.id == (player + i) and p.diceAmount > 0:
                return p.id
    for p in playersList:
        if p.diceAmount > 0 and p.id != player:
            return p.id
    print("HVAD FANDEN FOREGÅR DER")
    exit()

def playRound(player, lastGuess, lastPlayer):
    # Helping function
    displayPlayers(player, lastGuess)
    global playerTurnLabel
    if not playerTurnLabel:
        playerTurnLabel = tk.Label(root, text=player)
        playerTurnLabel.pack()
    else:
        playerTurnLabel.text=player
    nextPlayerId = nextPlayer(player)

    if not lastGuess:
        playerGuess = find_guess()
        playRound(nextPlayerId, playerGuess, player)
    elif checkGuess():
        playerGuess = find_guess()
        if validGuess(playerGuess, lastGuess):
            playRound(nextPlayerId, playerGuess, player)
        else:
            print("Invalid guess!")
            exit()
    else:
        if guessIsTrue(lastGuess):
            newRound(player)
        else:
            newRound(lastPlayer)

# ----------------------------------------------------------------------------------------------------Validering

def validGuess(guess, lastGuess):
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
        for i in range(len(diceRoll) - 1):
            if (diceRoll[i] + 1) != diceRoll[i + 1]:
                return False
    else:
        return False
    return True

def guessIsTrue(guess):
    result = checkAllDices()
    if guess[1] == "k":
        for r in result:
            if result[r] >= int(guess[0]):
                return True
        return False
    if int(guess[0]) <= result[int(guess[1])]:
        return True
    return False

def checkAllDices():
    result = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for p in playersList:
        if checkForStair(p.diceRoll):
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



# ----------------------------------------------------------------------------------------------------Helping Function





def displayPlayers(player, lastGuess):
    for widget in player_frame.winfo_children():
        widget.destroy()
    
    for p in playersList:
        tk.Label(player_frame, text=f"Player {p.id}: Dice Amount = {p.diceAmount}, Dice Roll = {p.diceRoll}", font=("Helvetica", 12)).pack(pady=5)

    
    global playerTurnLabel, diceResult, lastGuessLabel

    round_result = checkAllDices()
    if not playerTurnLabel:
        playerTurnLabel = tk.Label(root, text=round_result)
        playerTurnLabel.pack()
    else:
        playerTurnLabel.text=round_result
    if not diceResult:
        diceResult = tk.Label(root, text=f"player {player}'s turn")
        diceResult.pack()
    else:
        playerTurnLabel.text=f"player {player}'s turn"
    if not lastGuessLabel:
        lastGuessLabel = tk.Label(root, text="You place the first bet")
        lastGuessLabel.pack()
    else:
        lastGuessLabel.text = f"Last Player Said {lastGuess}"
    print("CHECK DONE")


# ----------------------------------------------------------------------------------------------------Tkinter


# Initialize the main window
root = tk.Tk()
root.title("Thinking Box")    
root.geometry("800x600+100+50")

player_frame = tk.Frame(root)
player_frame.pack(pady=20)

startGame()

# Run the main loop
root.mainloop()


