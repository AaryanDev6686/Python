#Define menu
menu = {
    'pizza': 40,
    'pasta': 50,
    'burger': 60,
    'salad': 70,
    'coffee': 80,
    'sandwich': 90,
}
#Greet
print("Welcome to PYTHON Restaurant!")
#Display menu
print("Here is our menu:\npizza : Rs40\npasta : Rs50\nburger : Rs60\nsalad : Rs70\ncoffee : Rs80\nsandwich : Rs90")
#Order System
order_total = 0
while True:
    item_1 = input("Enter the name of item you want to order: ").lower()
    if item_1 in menu:
        order_total += menu[item_1]
        print(f"Item, {item_1} has been added to order")
    else:
        print(f"Item, {item_1} is not available!")
    #Ask user if anything else is left to order
    more = input("Do you want to order anything else ").lower()
    if more == 'no':
         
         break
#Display total bill
print(f"Total amount of bill to pay is Rs{order_total}")
