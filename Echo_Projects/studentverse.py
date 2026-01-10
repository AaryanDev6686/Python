# ==================================================
# STUDENTVERSE - LEGENDARY EDITION
# Created by: Aaryan
# Powered by: Echo 😎
# ==================================================

import os

USER_FILE = "users.txt"
SCORE_FILE = "quiz_scores.txt"
NOTES_FILE = "notes.txt"
PLAN_FILE = "planner.txt"

current_user = None

# ------------------ UTILITIES ------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("\nPress Enter to continue...")

# ------------------ BANNER ------------------

def banner():
    print("=" * 50)
    print("        STUDENTVERSE - LEGENDARY")
    print("     Learn | Play | Plan | Grow")
    print("=" * 50)

# ------------------ AUTH SYSTEM ------------------

def register():
    clear()
    banner()
    print("📝 REGISTER")

    username = input("Choose username: ")
    password = input("Choose password: ")

    with open(USER_FILE, "a") as f:
        f.write(username + "," + password + "\n")

    print("✅ Registration successful!")
    pause()

def login():
    global current_user
    clear()
    banner()
    print("🔐 LOGIN")

    username = input("Username: ")
    password = input("Password: ")

    try:
        with open(USER_FILE, "r") as f:
            for line in f:
                u, p = line.strip().split(",")
                if u == username and p == password:
                    current_user = username
                    print("✅ Login successful!")
                    pause()
                    return
    except FileNotFoundError:
        pass

    print("❌ Invalid login!")
    pause()

# ------------------ QUIZ ENGINE ------------------

def quiz_zone():
    clear()
    banner()
    print("🧠 QUIZ ZONE")

    questions = [
        ("What is 2 + 2?", "4"),
        ("Capital of India?", "delhi"),
        ("Which language is this project in?", "python"),
    ]

    score = 0

    for q, ans in questions:
        print("\nQ:", q)
        user_ans = input("Answer: ").lower()
        if user_ans == ans:
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")

    print("\n🏆 Your Score:", score, "/", len(questions))

    with open(SCORE_FILE, "a") as f:
        f.write(current_user + ":" + str(score) + "\n")

    pause()

# ------------------ GAMES ZONE ------------------

def games_zone():
    clear()
    banner()
    print("🎮 GAMES ZONE")
    print("1. Number Guess")
    print("2. Back")

    choice = input("Choose: ")

    if choice == "1":
        number_guess()

def number_guess():
    import random
    secret = random.randint(1, 10)
    tries = 3

    while tries > 0:
        guess = int(input("Guess number (1-10): "))
        if guess == secret:
            print("🎉 You win!")
            pause()
            return
        else:
            tries -= 1
            print("Wrong! Tries left:", tries)

    print("😢 You lost! Number was:", secret)
    pause()

# ------------------ NOTES MANAGER ------------------

def notes_manager():
    clear()
    banner()
    print("📝 NOTES")
    print("1. Write Note")
    print("2. View Notes")

    choice = input("Choose: ")

    if choice == "1":
        note = input("Write your note:\n")
        with open(NOTES_FILE, "a") as f:
            f.write(current_user + ": " + note + "\n")
        print("✅ Saved!")
    elif choice == "2":
        try:
            with open(NOTES_FILE, "r") as f:
                print("\n--- NOTES ---")
                print(f.read())
        except FileNotFoundError:
            print("No notes found.")

    pause()

# ------------------ STUDY PLANNER ------------------

def study_planner():
    clear()
    banner()
    print("📅 STUDY PLANNER")

    plan = input("Enter today's study plan:\n")
    with open(PLAN_FILE, "a") as f:
        f.write(current_user + ": " + plan + "\n")

    print("✅ Plan saved!")
    pause()

# ------------------ PROGRESS TRACKER ------------------

def progress_tracker():
    clear()
    banner()
    print("📊 PROGRESS")

    try:
        with open(SCORE_FILE, "r") as f:
            for line in f:
                if line.startswith(current_user):
                    print("Quiz ->", line.strip())
    except FileNotFoundError:
        print("No progress yet.")

    pause()

# ------------------ MAIN MENU ------------------

def main_menu():
    while True:
        clear()
        banner()
        print("Logged in as:", current_user)
        print("""
1. Quiz Zone
2. Games Zone
3. Notes Manager
4. Study Planner
5. Progress Tracker
6. Logout
""")
        choice = input("Choose: ")

        if choice == "1":
            quiz_zone()
        elif choice == "2":
            games_zone()
        elif choice == "3":
            notes_manager()
        elif choice == "4":
            study_planner()
        elif choice == "5":
            progress_tracker()
        elif choice == "6":
            break

# ------------------ START ------------------

while True:
    clear()
    banner()
    print("""
1. Login
2. Register
3. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        login()
        if current_user:
            main_menu()
    elif choice == "2":
        register()
    elif choice == "3":
        print("👋 Bye Aaryan!")
        break
