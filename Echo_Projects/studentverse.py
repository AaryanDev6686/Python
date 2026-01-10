#!/usr/bin/env python3
# ==================================================
# STUDENTVERSE - LEGENDARY EDITION (Refactored)
# Created by: Aaryan (original)
# Refactor/Hardening: Assistant
# Features:
#  - SQLite-backed storage (users, quiz_scores, notes, plans)
#  - Secure password hashing (PBKDF2-HMAC-SHA256)
#  - Input validation and robust error handling
#  - Timestamps and better UX
# ==================================================

import os
import sys
import sqlite3
import hashlib
import secrets
import getpass
import datetime
from pathlib import Path
from typing import Optional, Tuple, List

DB_NAME = "studentverse.db"
CLEAR_CMD = "cls" if os.name == "nt" else "clear"


# ------------------ UTILITIES ------------------

def clear():
    os.system(CLEAR_CMD)

def pause(prompt: str = "\nPress Enter to continue..."):
    input(prompt)

def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat(sep=" ", timespec="seconds")

def safe_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    while True:
        s = input(prompt).strip()
        try:
            val = int(s)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if min_value is not None and val < min_value:
            print(f"Value must be >= {min_value}.")
            continue
        if max_value is not None and val > max_value:
            print(f"Value must be <= {max_value}.")
            continue
        return val

def prompt_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")

def prompt_choice(prompt: str, choices: List[str]) -> str:
    choices_set = set(choices)
    while True:
        s = input(prompt).strip()
        if s in choices_set:
            return s
        print(f"Invalid choice. Choose one of: {', '.join(choices)}")


# ------------------ SECURITY (password hashing) ------------------

def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
    """
    Returns (salt_hex, hash_hex). If salt given, reuse it; else generate new 16-byte salt.
    Uses PBKDF2-HMAC-SHA256 with 200_000 iterations.
    """
    if salt is None:
        salt = secrets.token_bytes(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return salt.hex(), hash_bytes.hex()

def verify_password(stored_salt_hex: str, stored_hash_hex: str, provided_password: str) -> bool:
    salt = bytes.fromhex(stored_salt_hex)
    _, hash_hex = hash_password(provided_password, salt)
    return secrets.compare_digest(hash_hex, stored_hash_hex)


# ------------------ DATABASE LAYER ------------------

class Storage:
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = Path(db_path)
        self._ensure_db()

    def _connect(self):
        return sqlite3.connect(str(self.db_path), timeout=10, isolation_level=None)

    def _ensure_db(self):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                pw_salt TEXT NOT NULL,
                pw_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS quiz_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plan TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)
        finally:
            conn.close()

    # Users
    def create_user(self, username: str, password: str) -> bool:
        salt_hex, hash_hex = hash_password(password)
        created_at = now_iso()
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, pw_salt, pw_hash, created_at) VALUES (?, ?, ?, ?)",
                        (username, salt_hex, hash_hex, created_at))
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def get_user(self, username: str) -> Optional[Tuple[int, str, str, str]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, username, pw_salt, pw_hash FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            if row:
                return row  # (id, username, pw_salt, pw_hash)
            return None
        finally:
            conn.close()

    # Quiz Scores
    def add_quiz_score(self, user_id: int, score: int, total: int):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO quiz_scores (user_id, score, total, created_at) VALUES (?, ?, ?, ?)",
                        (user_id, score, total, now_iso()))
        finally:
            conn.close()

    def get_quiz_scores_for_user(self, user_id: int) -> List[Tuple[int, int, str]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT score, total, created_at FROM quiz_scores WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            return cur.fetchall()
        finally:
            conn.close()

    # Notes
    def add_note(self, user_id: int, note: str):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO notes (user_id, note, created_at) VALUES (?, ?, ?)",
                        (user_id, note, now_iso()))
        finally:
            conn.close()

    def get_notes_for_user(self, user_id: int) -> List[Tuple[str, str]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT note, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            return cur.fetchall()
        finally:
            conn.close()

    # Plans
    def add_plan(self, user_id: int, plan: str):
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO plans (user_id, plan, created_at) VALUES (?, ?, ?)",
                        (user_id, plan, now_iso()))
        finally:
            conn.close()

    def get_plans_for_user(self, user_id: int) -> List[Tuple[str, str]]:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT plan, created_at FROM plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
            return cur.fetchall()
        finally:
            conn.close()


# ------------------ APP (business logic + UI) ------------------

class StudentVerse:
    def __init__(self):
        self.storage = Storage()
        self.current_user_id: Optional[int] = None
        self.current_username: Optional[str] = None
        self.questions = [
            ("What is 2 + 2?", "4"),
            ("Capital of India?", "delhi"),
            ("Which language is this project in?", "python"),
        ]

    # BANNER
    def banner(self):
        print("=" * 50)
        print("        STUDENTVERSE - LEGENDARY")
        print("     Learn | Play | Plan | Grow")
        print("=" * 50)

    # AUTH
    def register(self):
        clear()
        self.banner()
        print("📝 REGISTER")
        username = prompt_nonempty("Choose username: ").lower()
        # Use getpass for password so it won't echo on screen
        while True:
            password = getpass.getpass("Choose password: ")
            if not password:
                print("Password cannot be empty.")
                continue
            password2 = getpass.getpass("Confirm password: ")
            if password != password2:
                print("Passwords do not match. Try again.")
                continue
            break

        success = self.storage.create_user(username, password)
        if success:
            print("✅ Registration successful!")
        else:
            print("❌ Username already exists. Pick another username.")
        pause()

    def login(self):
        clear()
        self.banner()
        print("🔐 LOGIN")
        username = prompt_nonempty("Username: ").lower()
        password = getpass.getpass("Password: ")
        user = self.storage.get_user(username)
        if user is None:
            print("❌ Invalid username or password.")
            pause()
            return False
        user_id, _, pw_salt, pw_hash = user
        if verify_password(pw_salt, pw_hash, password):
            self.current_user_id = user_id
            self.current_username = username
            print("✅ Login successful!")
            pause()
            return True
        else:
            print("❌ Invalid username or password.")
            pause()
            return False

    def logout(self):
        self.current_user_id = None
        self.current_username = None
        print("Logged out.")
        pause()

    # QUIZ
    def quiz_zone(self):
        clear()
        self.banner()
        print("🧠 QUIZ ZONE")
        score = 0
        total = len(self.questions)
        for q, ans in self.questions:
            print("\nQ:", q)
            user_ans = prompt_nonempty("Answer: ").lower()
            if user_ans == ans:
                print("✅ Correct!")
                score += 1
            else:
                print("❌ Wrong! (Expected: {})".format(ans))
        print("\n🏆 Your Score:", score, "/", total)
        if self.current_user_id:
            self.storage.add_quiz_score(self.current_user_id, score, total)
        pause()

    # GAMES
    def games_zone(self):
        clear()
        self.banner()
        print("🎮 GAMES ZONE")
        print("1. Number Guess")
        print("2. Back")
        choice = prompt_choice("Choose: ", ["1", "2"])
        if choice == "1":
            self.number_guess()

    def number_guess(self):
        import random
        secret = random.randint(1, 10)
        tries = 3
        print("Guess the secret number between 1 and 10. You have 3 tries.")
        while tries > 0:
            guess = safe_int("Guess number (1-10): ", 1, 10)
            if guess == secret:
                print("🎉 You win!")
                pause()
                return
            else:
                tries -= 1
                print("Wrong! Tries left:", tries)
        print("😢 You lost! Number was:", secret)
        pause()

    # NOTES
    def notes_manager(self):
        clear()
        self.banner()
        print("📝 NOTES")
        print("1. Write Note")
        print("2. View Notes")
        print("3. Back")
        choice = prompt_choice("Choose: ", ["1", "2", "3"])
        if choice == "1":
            note = prompt_nonempty("Write your note:\n")
            if self.current_user_id:
                self.storage.add_note(self.current_user_id, note)
                print("✅ Saved!")
        elif choice == "2":
            if self.current_user_id:
                notes = self.storage.get_notes_for_user(self.current_user_id)
                if not notes:
                    print("No notes found.")
                else:
                    print("\n--- NOTES (most recent first) ---")
                    for note, created_at in notes:
                        print(f"[{created_at}] {note}")
            else:
                print("No user logged in.")
        pause()

    # PLANNER
    def study_planner(self):
        clear()
        self.banner()
        print("📅 STUDY PLANNER")
        plan = prompt_nonempty("Enter today's study plan:\n")
        if self.current_user_id:
            self.storage.add_plan(self.current_user_id, plan)
            print("✅ Plan saved!")
        pause()

    # PROGRESS
    def progress_tracker(self):
        clear()
        self.banner()
        print("📊 PROGRESS")
        if self.current_user_id:
            scores = self.storage.get_quiz_scores_for_user(self.current_user_id)
            if not scores:
                print("No quiz progress yet.")
            else:
                print("\n--- QUIZ SCORES (most recent first) ---")
                for score, total, created_at in scores:
                    print(f"[{created_at}] {score}/{total}")
        else:
            print("No user logged in.")
        pause()

    # MAIN MENU
    def main_menu(self):
        while self.current_user_id:
            clear()
            self.banner()
            print("Logged in as:", self.current_username)
            print("""
1. Quiz Zone
2. Games Zone
3. Notes Manager
4. Study Planner
5. Progress Tracker
6. Logout
""")
            choice = prompt_choice("Choose: ", ["1", "2", "3", "4", "5", "6"])
            if choice == "1":
                self.quiz_zone()
            elif choice == "2":
                self.games_zone()
            elif choice == "3":
                self.notes_manager()
            elif choice == "4":
                self.study_planner()
            elif choice == "5":
                self.progress_tracker()
            elif choice == "6":
                self.logout()

    # START LOOP
    def run(self):
        try:
            while True:
                clear()
                self.banner()
                print("""
1. Login
2. Register
3. Exit
""")
                choice = prompt_choice("Choose: ", ["1", "2", "3"])
                if choice == "1":
                    if self.login():
                        self.main_menu()
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    print(f"👋 Bye {self.current_username or 'friend'}!")
                    break
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
        except Exception as e:
            print("An unexpected error occurred:", e)
        finally:
            pass


if __name__ == "__main__":
    app = StudentVerse()
    app.run()