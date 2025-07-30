import math

def addition():
    return num1 + num2
def subtraction():
    return num1 - num2
def division():
    return num1 / num2
def multiply():
    return num1 * num2
def power():
    return math.pow(num1, num2)
def square_root():
    return math.sqrt(num1) 

print ("Welcome to calculator program (input 2 numbers only)")
print ("-"*50)

while True:
    print ("Enter 1 to add")
    print ("Enter 2 to subtract")
    print ("Enter 3 to divide")
    print ("Enter 4 to multiply")
    print ("Enter 5 to raise a number to a power")
    print ("Enter 6 to square root")
    print ("Enter 7 to exit from the calculator")
    choice = int(input("Enter your choice = "))
   
    if (choice == 1):
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        print(f"{num1} + {num2} = {addition()}")
    elif (choice == 2):
       num1 = int(input("Enter the first number: "))
       num2 = int(input("Enter the second number: "))
       print(f"{num1} - {num2} = {subtraction()}")
    elif (choice == 3):
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        if num2 == 0:
            print("ERROR! Undefined")
        else:
            print(f"{num1} / {num2} = {division()}")
            break
    elif (choice == 4):
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        print(f"{num1} X {num2} = {multiply()}")
    elif (choice == 5):
        num1 = float(input("Enter a number: "))
        num2 = int(input("Enter the power of that number: "))
        print(f"The power of {num1} = {power()}")
    elif (choice == 6):
        num1 = int(input("Enter a number: "))
        print(f"The square of {num1} = {square_root()}")
    elif (choice == 7):
        print("Thanks for calculating with us, See ya!")
        break
    else:
        print("Enter the invalid input")
        

         
        


