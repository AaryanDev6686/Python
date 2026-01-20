import random

options = ("rock", "paper", "scissors")

computer = random.choice(options)

while True:
    player = input("Enter your choice (rock, paper, scissors)").lower()
    if player not in options:
        print("Invalid choice! Try again")
    print(f"Player: {player}\nComputer: {computer}")

    if player == computer:
        print("It's a tie")
    elif player == "rock" and computer == "scissors":
        print("You win!")
    elif player == "scissors" and computer == "paper":
        print("You win!")
    elif player == "paper" and computer == "rock":
        print("You win!")
    
    else:
        print("You lose!")

    play_again = input("Do you want to play again? (y/n)").lower()
    if  play_again != "y":
        break

print("Thanks for playing")