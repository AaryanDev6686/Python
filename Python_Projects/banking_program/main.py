#Python Banking Program

balance = 0

while True:
    print("\n1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Choose (1-4): ")

    if choice == "1":
        print(f"Balance: {balance:.2f}")
    elif choice == "2":
        amount = float(input("Enter the amount you want to deposit "))
        if amount > 1:
            balance += amount 
        else:
            print("Enter a amount greater than zero")
    elif choice == "3":
        amount = float(input("Withdraw amount: "))
        if amount < balance:
            balance += amount
        else:
            print("Invalid withdrawl amount")
    elif choice == "4":
        break
    
    else:
        print("Wrong choice")

print("Goodbye! Have a nice day")
