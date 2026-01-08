#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    # Returns the cost of the shoes
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f'''Product:{self.product},
 Country:{self.country}, 
 Cost:{self.cost}, 
 Quantity:{self.quantity}, 
 Code:{self.code}'''


#=============Shoe list===========
# This list will be used to store a list of shoe objects
shoe_list = []

#==========Functions outside the class==============
# Reads the file inventory.txt to create shoe objects
# The shoe objects will then be appended to shoe_list
def read_shoes_data():
    # Opens the inventory text file
    with open("inventory.txt", "r") as file:
        # Transforms the file's lines into a list
        lines = file.readlines()
        # Itterates over each line skipping the first
        for line in lines[1:]:
            # Removes next line notation from string
            # then converts the line into a list of attributes from a string
            vals = (line.replace("\n","")).split(",")
            # Creates a Shoe object using attributes
            try: 
                new_shoe = Shoe(vals[0],vals[1],vals[2],vals[3],(vals[4]))
                shoe_list.append(new_shoe)
            except:
                line_num = lines.index(line)
                print(f'''Error: on line {line_num} of inventory.txt 
this line has not been processed''')

# Allows user to input data about a shoe and add it to the shoe list
def capture_shoes():
    code = input("Enter the shoe code: ")
    # Check to see if the code already exists
    old_shoe = search_shoe(code)
    # If it does not already exist continue
    if old_shoe == None:
        # Obtains the rest of the information for the new shoe from user
        country = input("Enter the shoe country:")
        product = input("Enter the shoe name:")
        cost = input("Enter the shoe cost:")
        quantity = input("Enter the shoe quantity:")
        # Creates the new shoe and appends it to shoe_list
        try:
            new_shoe = Shoe(country, code, product, cost, quantity)
        except:
            print("Error: one of your inputs was invalid")
            print("Try again, quantity and cost must be integers")
            capture_shoes()
            return
        # While loop to get confirmation from user and handle incorrect inputs
        while True:
            confirmation = input(f'''Add new shoe type with the following attributes:
{new_shoe}?
to confirm type "confirm" to cancel type "cancel"
''')
            #adds the new shoe to the list and then the inventory
            if confirmation == "confirm":
                shoe_list.append(new_shoe)
                update_inventory()
                break
            # cancels the process
            elif confirmation == "cancel":
                return
            else:
                print('Please input either "confirm" or "cancel"')
    # If the code already exists warn user and restart function
    else:
        print(f"This code is already assigned to {old_shoe.product}")
        capture_shoes()

def view_all():
    for shoe in shoe_list:
        print(shoe)
        print()

def re_stock():
    # Calls a function to sort by quantity
    quantity_sort(shoe_list, 0, len(shoe_list) - 1)
    low_shoe = shoe_list[0]
    current_stock = shoe_list[0].quantity
    new_stock = int(input(f'''{low_shoe.product}s have the lowest stock
How many have been restocked?
'''))
    shoe_list[0].quantity = current_stock + new_stock
    update_inventory()

def search_shoe(target):
    # The list is itterated over.
    # If an object with the code is found, it is returned.
    for index in range(len(shoe_list)): 
        if (shoe_list[index]).code == target: 
            return shoe_list[index]
    # If the code is not found, None is returned. 
    return None

def value_per_item():
    for shoe in shoe_list:
        value = shoe.quantity * shoe.cost
        print(f"{shoe.product}: {value}")

def highest_qty():
    # Calls a function to sort by quantity
    quantity_sort(shoe_list, 0, len(shoe_list) - 1)
    #Prints that the highest quantity shoe is for sale
    print(f"{shoe_list[-1].product} is for sale")

# Sorts shoe list by ascending quantity, using quick sort method
def quantity_sort(items, low, high):
    if low < high:
        # Calls partition function to get the pivot index
        mid = partition(items, low, high)
        # Recursively sorts the left partition
        items = quantity_sort(items, low, mid - 1)
        # Recursively sorts the right partition
        items = quantity_sort(items, mid + 1, high)
 
    return items

def partition(items, low, high):
    pivot = items[low]
    while low < high:
        while low < high and (items[high]).quantity >= pivot.quantity:
            high -= 1
        if low < high:
            items[low] = items[high]
            while low < high and (items[low]).quantity <= pivot.quantity:
                low += 1
            if low < high:
                items[high] = items[low]
    items[low] = pivot
    return low

# Updates the inventory.txt file based off of shoe_list
def update_inventory():
    inventory = "Country,Code,Product,Cost,Quantity\n"
    for shoe in shoe_list:
        nextline = f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n"
        inventory = inventory + nextline
    inventory = inventory[:-1]
    with open("inventory.txt", "w") as file:
        file.write(inventory)

#==========Main Menu=============
# Calls the read shoes function to fill shoe_list
read_shoes_data()

while True:
    # requests operation input from user
    operation = input('''Which Operation would you like to use?:
"search" - Print the information of a shoe based on a code
"add" - Add a new shoe to the shoe list
"restock" - Add stock to the shoe with the least stock
"sale" - Find the shoe with the most stock and prints a sale message
"view all" - Lists all the products and their information
"list values" - List the total values of the stock of each shoe
"close" - close the application
''')
    # Determines the operation the user input
    if operation == "search":
        result = search_shoe(input("Enter a shoe code: "))
        if result != None:
            print(result)
        else:
            print("Error: Code not found")
    elif operation == "add":
        capture_shoes()
    elif operation == "restock":
        re_stock()
    elif operation == "sale":
        highest_qty()
    elif operation == "view all":
        view_all()
    elif operation == "list values":
        value_per_item()
    elif operation == "close":
        break
    # incase of an invalid operation, warns the user
    else:
        print("Error: Invalid operation")