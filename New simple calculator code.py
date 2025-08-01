import math
def add(*args):
    return sum(args)
def subtract(*args):
    result = args[0]
    for arg in args[1:]:
        result -= arg
    return result 
def multiply(*args):
    result = 1
    for arg in args:
        result *= arg
    return result
def divide(*args):
    result = args[0]
    for arg in args[1:]:
        if arg == 0:
            return "ERROR! Division by zero is undefined"
        result /= arg
    return result
def power(num1, num2):
    return math.pow(num1, num2)
def square_root(num1):
    return math.sqrt(num1) if num1 >= 0 else "ERRO! Negative number"

print("Welcome to calculator program")
print("-" *33 )
print("Calculator Operations:")
print("Enter 1 to Add")
print("Enter 2 to Subtract")
print("Enter 3 to Multiply")
print("Enter 4 to Divide")
print("Enter 5 Power")
print("Enter 6 Square root")
print("Press 7 to quit the program")

while True:
    choice = input("Enter operation (or Press '7' to quit): ").lower()
    if choice == '7':
        break
    if choice in ['1', '2', '3', '4']:
        args = list(map(float,input("Please enter numbers separated by space: ").split()))
        if choice == '1':
            print("Result = ", add(*args))
        elif choice == '2':
            print("Result = ", subtract(*args))
        elif choice == '3':
            print("Result = ", multiply(*args))
        elif choice == '4':
            print("Result = ", divide(*args)) 
    if choice in ['5']:  
        if choice == '5':
            num1 = float(input("Base: "))
            num2 = float(input("Exponent: "))
            print("Result = ", power(num1, num2))
    if choice in ['6']:  
        if choice == '6':
            num1 = float(input("Enter a number: "))
            print("Result = ", square_root(num1))
    





