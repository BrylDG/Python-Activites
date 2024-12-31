'''
    Simple Sales System
'''
from os import system, path

itemfile: str = "items.csv"
cartfile: str = "cart.csv"
itemsheader: list = ['itemcode', 'description', 'price']
cartheader: list = ['#', 'itemcode', 'description', 'price', 'qty', 'total']

cartno: int = 0
cart: str = ""
itemcode: str = ""
description: str = ""
price: str = ""
qty: str = ""
total: str = ""
item: str = ""
data: list = []

index: int = 999999


def main() -> None:
    option: int = -1
    while option != 0:
        displaymenu()
        try:
            option = int(input("Enter Option (0...3): "))
            match option:
                case 1: buy_items()
                case 2: show_cart()
                case 3: show_items()
                case 0: terminate()

        except Exception as e:
            print(f"Input Error: Only 0 to 3!")
        print()
        input("Press Any Key to Continue...")


def displaymenu() -> None:
    system('cls')
    print('-' * 5 + ' Main Menu ' + '-' * 5)
    print('1. Buy Item')
    print('2. Show Cart')
    print('3. Show Items')
    print('0. Quit/End')
    print('-' * 21)


def function_header(title: str) -> None:
    system('cls')
    print("-" * 20)
    print(title.upper().center(20))
    print("-" * 20)


def validate_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty or whitespace. Please try again.")
        else:
            return value


def buy_items() -> None:
    global itemcode, description, price, qty, total, cart, cartno
    function_header('BUY ITEMS')
    find_items()


def buy_module() -> None:
    global itemcode, description, price, qty, total, cart, cartno
    qty = validate_input("qty: ")
    
    if int(qty) == 0:
        print("-"*1)
        print("0 Items bought. Exiting")
        return
        
    num: float = float(qty)
    itemprice: float = float(price)
    total = str(f"{itemprice * num:.2f}")
    print(f"TOTAL: {total}")
    print("")
    cartno += 1
    cart = str(cartno)
    data_item: list = [cart, itemcode, description, price, qty, total]
    print("Item Bought...")
    mydata: str = ",".join(data_item)
    with open(cartfile, 'a') as file:
        file.write(mydata + "\n")


def find_items() -> None:
    global itemcode, description, price, qty, total
    file = open(itemfile)
    data = file.readlines()
    file.close()
    trig: int = 0
    itemcode = validate_input("ITEMCODE      : ")
    for item in data:
        fields: list = item.strip().split(',')
        if itemcode == fields[0]:
            index = data.index(item)
            description = fields[1]
            price = fields[2]
            print(f"{itemsheader[1]} : {fields[1]}")
            print(f"{itemsheader[2]} : {fields[2]}")
            buy_module()
            trig = 1
            break
    if trig == 0:
        print("Item not found...")

def totalamount(cart_data: list) -> float:
    totalamount: float = 0.0
    for item in cart_data:
        fields: list = item.strip().split(',')
        if len(fields) < 6:
            continue
        try:
            itemprice: float = float(fields[5])
            totalamount += itemprice
        except ValueError:
            continue
    return totalamount


def show_cart() -> None:
    global cartfile, cartheader
    system("cls")
    file = open(cartfile)
    cartitems: list = file.readlines()
    file.close()
    print("-" * 110)
    [print(f"{head.upper():<20}", end="") for head in cartheader]
    print()
    print("-" * 110)
    for index in cartitems:
        index = index.strip()
        fields: list = index.split(',')
        [print(f"{item:<20}", end="") for item in fields]
        print()
    print("-" * 110)
    total: float = totalamount(cartitems)
    print(f"{'TOTAL:':>99} {total:.2f}")
    print("-" * 110)


def show_items() -> None:
    system("cls")
    file = open(itemfile)
    print("-" * 100)
    [print(f"{head.upper():<20}", end="") for head in itemsheader]
    print()
    print("-" * 100)
    for index in file:
        index: str = index.strip()
        fields: list = index.split(',')
        [print(f"{item:<20}", end="") for item in fields]
        print()
    print("-" * 100)
    file.close()


def terminate() -> None:
    print('Program Ended...')


if __name__ == "__main__":
    main()
