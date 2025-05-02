import random

def get_computer_choice():
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    score_user = 0
    score_computer = 0
    history_user = []
    history_computer = []
    
    print("Welcome to Rock-Paper-Scissors!")

    while True:
        print("\nChoose one: Rock, Paper, or Scissors")
        user_choice = input().lower()
        
        if user_choice not in ["rock", "paper", "scissors"]:
            print("Invalid choice, please choose Rock, Paper, or Scissors.")
            continue
        
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        
        result = determine_winner(user_choice, computer_choice)
        print(result)
        
        if result == "You win!":
            score_user += 1
        elif result == "You lose!":
            score_computer += 1
        
        history_user.append(user_choice)
        history_computer.append(computer_choice)
        
        print(f"\nScore - You: {score_user} | Computer: {score_computer}")
        
        print("\nGame History:")
        for i in range(len(history_user)):
            print(f"Round {i+1}: You chose {history_user[i]}, Computer chose {history_computer[i]}")
        
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

def best_of_three():
    score_user = 0
    score_computer = 0
    round_count = 0
    
    print("\nWelcome to Best of 3 - Rock-Paper-Scissors!")

    while round_count < 3:
        print(f"\nRound {round_count+1}: Choose one: Rock, Paper, or Scissors")
        user_choice = input().lower()
        
        if user_choice not in ["rock", "paper", "scissors"]:
            print("Invalid choice, please choose Rock, Paper, or Scissors.")
            continue
        
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")
        
        result = determine_winner(user_choice, computer_choice)
        print(result)
        
        if result == "You win!":
            score_user += 1
        elif result == "You lose!":
            score_computer += 1
        
        round_count += 1
        
        print(f"\nScore - You: {score_user} | Computer: {score_computer}")
        
        if score_user > 1 or score_computer > 1:
            break
    
    if score_user > score_computer:
        print("\nYou won the best of 3!")
    elif score_computer > score_user:
        print("\nComputer won the best of 3!")
    else:
        print("\nIt's a tie!")

def main():
    while True:
        print("\nChoose game mode:")
        print("1. Player vs Computer")
        print("2. Best of 3 (Player vs Computer)")
        print("3. Player vs Player")
        print("4. Exit")
        
        mode = input("Enter your choice (1/2/3/4): ").strip()

        if mode == "1":
            play_game()
        elif mode == "2":
            best_of_three()
        elif mode == "3":
            print("Player vs Player is under development!")
        elif mode == "4":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice, please enter a valid number.")

# Start the game
main()
