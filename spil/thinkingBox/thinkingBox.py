import random
import tkinter as tk
from tkinter import simpledialog, messagebox

startDiceAmount = 2
playersAmount = 3
playersList = []
lastPlayer = None
guessAmount = None
guessValue = None
class PlayerInformation:
    def __init__(self, id, diceAmount, diceRoll):
        self.id = id
        self.diceAmount = diceAmount 
        self.diceRoll = diceRoll

def rollDices(d):
    return [random.randint(1,6) for _ in range(d)]

def startGame():
    global playersList
    playersList = [PlayerInformation(i, startDiceAmount, None) for i in range(playersAmount)]
    newRound(None)

def find_guess():
    def submit_guess():
        root.quit()  # Ends the Tkinter main loop


    guessAmount = tk.IntVar()  # Define guessAmount as an IntVar
    guessValue = tk.StringVar()  # Define guessValue as an IntVar

    # Frame for the first group of radio buttons
    frame1 = tk.Frame(root)
    frame1.pack(pady=(10, 0))  # Add padding on top and no padding at bottom

    # Create and pack radio buttons for guessAmount
    amountOfDices = sum(p.diceAmount + 1 for p in playersList)
    for i in range(1,amountOfDices + 1):
        tk.Radiobutton(frame1, text=i, variable=guessAmount, value=i).pack(side=tk.LEFT, padx=5, pady=5)

    # Add an empty frame to create space
    spacer_frame = tk.Frame(root, height=20)  # Create a spacer frame with a specific height
    spacer_frame.pack()  # Pack the spacer frame to create space between groups

    # Frame for the second group of radio buttons
    frame2 = tk.Frame(root)
    frame2.pack()

    # Create and pack radio buttons for guessValue
    for i in range(1, ):
        tk.Radiobutton(frame2, text=i, variable=guessValue, value=i).pack(side=tk.LEFT, padx=10, pady=10)

    # Additional radio button for guessValue
    tk.Radiobutton(frame2, text="kind", variable=guessValue, value="k").pack(side=tk.LEFT, padx=10, pady=10)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=submit_guess)
    submit_button.pack(pady=10)

    root.mainloop()  # Start the mainloop to wait for user input

    selected_amount = guessAmount.get()
    selected_value = guessValue.get()
    print(selected_amount, selected_value)
    return selected_amount, selected_value  # Return the selected values

def checkGuess():
    def submit_guess():
        root.quit()  # Ends the Tkinter main loop

    decision = tk.BooleanVar()

    frame3 = tk.Frame(root)
    frame3.pack(pady=(10, 0))
    tk.Radiobutton(frame3, text="Open", variable=decision, value=False).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Radiobutton(frame3, text="Roll", variable=decision, value=True).pack(side=tk.LEFT, padx=10, pady=10)
    
    tk.Button(frame3, text="Submit", command=submit_guess).pack(pady=10)

    root.mainloop()
    selectedDecision = decision.get()
    
    print(selectedDecision,"DECISION!!!")
    return selectedDecision

def newRound(loosingPlayer):
    for p in playersList:
        if loosingPlayer and loosingPlayer != p.id:
            p.diceAmount -= 1
        if p.diceAmount < 1:
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
    exit()

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

def guessIsTrue(guess, result):
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

def playRound(player, lastGuess, lastPlayer):
    displayPlayers()

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
            root.quit()
    else:
        result = checkAllDices()
        if guessIsTrue(lastGuess, result):
            print("Result", f"Player {player} lost!")
        else:
            print("Result", f"Player {lastPlayer} lost!")

# Initialize the main window
root = tk.Tk()
root.title("Thinking Box")    
root.geometry("800x600+100+50")

def displayPlayers():
    for widget in player_frame.winfo_children():
        widget.destroy()
    
    for p in playersList:
        tk.Label(player_frame, text=f"Player {p.id}: Dice Amount = {p.diceAmount}, Dice Roll = {p.diceRoll}", font=("Helvetica", 12)).pack(pady=5)

def on_start_game():
    startGame()

# Create and place the button
button = tk.Button(root, text="Start Game", command=on_start_game, font=("Helvetica", 24))
button.pack(pady=20)

player_frame = tk.Frame(root)
player_frame.pack(pady=20)

# Run the main loop
root.mainloop()
