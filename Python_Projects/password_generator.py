import random
print("Welcome to Aaryan's Password Generator")
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#$%^&*().<>"
length = int(input("Enter a length: "))
password = ""

for i in range(length):
    password += random.choice(chars)
print(password)