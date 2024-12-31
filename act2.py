from os import system
import pwinput

a:int = 0
b:int = 0

def login()->None:
    print('cls')
    print("_"*7 + "LOG IN" + "_"*7)
    user: str = str(input("Enter Username: "))
    password: str = pwinput.pwinput("Enter Password: ")
    
    if user == "admin" and password == "hello123!":
        operations()
    else:
        print("Invalid Account!")

    
def inputSystem()->None:
    global a,b
    a = int(input("Enter first number:"))
    b = int(input("Enter second number:"))
    
def sum()->None:
    print("ADDITION")
    print("-"*20)
    inputSystem()
    print(f"sum of {a} and {b} is {(a+b)}")
    
def product()->None:
    print("MULTIPLICATION")
    print("-"*20)
    inputSystem()
    print(f"product of {a} and {b} is {(a*b)}")
    
def difference()->None:
    print("SUBTRACTION")
    print("-"*20)
    inputSystem()
    print(f"difference of {a} and {b} is {(a-b)}")

def quotient()->None:
    print("DIVISION")
    print("-"*20)
    inputSystem()
    print(f"quotient of {a} and {b} is {(a/b):.6f}")
    
def exponent()->None:
    print("EXPONENTIATION")
    print("-"*20)
    try:
        base:int = int(input("Base Number (1 - 20): "))
        power:int = int(input("Power Number (1 - 20): "))
        if base>0 and power <=20:
            print(f"{base} raised to the power of {power} is {(base**power)}")
        else:
            print("Invalid Input, Please try again!")
        
    except Exception as e:
       print(f"Input Error: {e}")

def terminate()->None:
    login()


def menu()->None:
    system("cls")
    print("-"*5+" MAIN MENU "+"-"*5)
    print("1. ADDITION")
    print("2. SUBTRACTION")
    print("3. MULTIPLICATION")
    print("4. DIVISION")
    print("5. EXPONENTIATION")
    print("0. QUIT/END")    
    print("-"*21)
    
def operations()->None:
    option:int = -1
    while option != 0:
        menu()
        try:
            option = int(input("Enter Option(0..5):"))
            if option == 1: 
                sum()
            elif option == 2: 
                difference()
            elif option == 3: 
                product()
            elif option == 4: 
                quotient()
            elif option == 5:
                exponent()
            elif option == 0: 
                terminate()
            else:
                print("Invalid Input: Only 0 to 5 !!!")
        except:
            print("Invalid Input")
        print()
        input("Press to continue...")
        
def main()->None:
    login()

if __name__ == "__main__":
    main()
    
