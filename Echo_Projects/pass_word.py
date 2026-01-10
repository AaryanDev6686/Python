# ================================
# MEGA USERNAME & PASSWORD MANAGER
# ================================

accounts = {}

# ---------- LOAD DATA ----------
try:
    file = open("data.txt", "r")
    for line in file:
        user, pwd = line.strip().split(",")
        accounts[user] = pwd
    file.close()
except:
    pass


# ---------- MASTER LOGIN ----------
print("🔐 Welcome to Password Manager")

master_user = "Aaryan"
master_pass = "6686"

u = input("Enter master username: ")
p = input("Enter master password: ")

if u != master_user or p != master_pass:
    print("❌ Access Denied")
    exit()

print("✅ Login Successful")


# ---------- MAIN MENU ----------
while True:
    print("\n------ MENU ------")
    print("1. Add account")
    print("2. View password")
    print("3. Update password")
    print("4. Delete account")
    print("5. Show all usernames")
    print("6. Exit")

    choice = input("Enter choice: ")

    # ADD ACCOUNT
    if choice == "1":
        user = input("Enter username: ")
        pwd = input("Enter password: ")
        accounts[user] = pwd
        print("✔ Account added")

    # VIEW PASSWORD
    elif choice == "2":
        user = input("Enter username: ")
        if user in accounts:
            print("Password:", accounts[user])
        else:
            print("❌ Account not found")

    # UPDATE PASSWORD
    elif choice == "3":
        user = input("Enter username: ")
        if user in accounts:
            new_pwd = input("Enter new password: ")
            accounts[user] = new_pwd
            print("✔ Password updated")
        else:
            print("❌ Account not found")

    # DELETE ACCOUNT
    elif choice == "4":
        user = input("Enter username: ")
        if user in accounts:
            del accounts[user]
            print("✔ Account deleted")
        else:
            print("❌ Account not found")

    # SHOW ALL USERNAMES
    elif choice == "5":
        if len(accounts) == 0:
            print("No accounts saved")
        else:
            print("Saved usernames:")
            for user in accounts:
                print("-", user)

    # EXIT
    elif choice == "6":
        file = open("data.txt", "w")
        for user, pwd in accounts.items():
            file.write(user + "," + pwd + "\n")
        file.close()
        print("💾 Data saved. Goodbye!")
        break

    else:
        print("❌ Invalid choice")
