#Cafe Shop Decision

#Name of the user
name = input("Enter your name: ")

#Decision 
pizza_decision = input(f"{name}, Do u like pizza? ")
if pizza_decision.lower() == 'yes':
    print(f"{name}, your order has been taken!")
else:
    another_order=input("Ok, vist us next time!")
