#Date:
#Authors:
#Assignment:

from datetime import datetime # Correctly import the datetime class

class Product:
    def __init__(self, item, price, stock): #intializing product attributes
       self.item = item
       self.price = price
       self.stock = stock

    def reduce_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        return False
    
    def is_low_stock(self): # Checks if stock is below the low-stock threshold (5)
        return self.stock < 5



class Store:
    def __init__(self):
        self.product_catalog = { #menu/catalog it prints when the customer selects add items to cart option
            "1": Product("Red Wine", 600, 20),
            "2": Product("Chicken", 400, 50),
            "3": Product("Orange Juice", 300, 30),
            "4": Product("Corn Beef", 400, 12),
            "5": Product("Spring Water", 500, 24),
            "6": Product("Pancake Mix", 300, 24),
            "7": Product("Lysol", 1000, 12),
            "8": Product("Coffee", 500, 20),
            "9": Product("Bread", 700, 12),
            "10": Product("Battery", 400, 36),
            "11": Product("Deodorant", 780, 12),
            "12": Product("Cooking Oil", 1000, 50),
            "13": Product("Egg", 900, 72),
            "14": Product("Laundry Detergent", 5000, 12),
            "15": Product("Rice", 300, 50),
            "16": Product("Apple", 700, 36),
            "17": Product("Banana", 800, 48),
            "18": Product("All Purpose Seasoning", 400, 24),
            "19": Product("Personal Care", 1000, 20),
            "20": Product("Cleaning Tools", 1800, 30),
        }

    def display_products(self):
        print("\nAvailable Products:")
        for key, product in self.product_catalog.items():
            stock_alert = " - LOW STOCK!" if product.is_low_stock() else ""  # if the item is less than 5 then this message will be beside the item on the menu saying low stock
            print(f"{key}. {product.item} - ${product.price} (Stock: {product.stock}){stock_alert}") #if the quantity is greater than 5 then the messagw will not be beside it


class Cart:
    def __init__(self):
        self.items = []  # Stores the product and the quantity
        
        # ... other methods ...
    def clear_cart(self):
        self.items = []  # Clear the cart

    def add_item(self, product, quantity): #add item method/function
        if product.reduce_stock(quantity):
            self.items.append((product, quantity))
            print(f"Successfully added {quantity} x {product.item} to the cart!\n") #output if the product is succesfully added
        else:
            print(f"Not enough stock for {product.item}.") #output if there was an incorrect quantoty

    def remove_item(self, index): #remove itme method/function 
        try: #its a loop that repeats until the user enters valid input
            removed_item = self.items[index - 1]  #finds the product based on the number given(index)
            del self.items[index - 1]  #removs the item at the given index
            print(f"{removed_item[0].item} removed from cart successfully!\n") #output if it succesfully removed
        except IndexError:
            print("Invalid selection. Please try again.")

    def view_cart(self, show_product=False): #view cart method
        if not self.items:
            print("\nYour cart is empty!\n") #if the cart is empty this error message will be printed
            return False

        print("\nItems in Your Cart:") #if there is items in the cart
        for idx, (item, quantity) in enumerate(self.items, start=1):
            print(f"{idx}. {item.item} - {quantity} x ${item.price} = ${item.price * quantity}")
        
        print(f"\nSubtotal: ${self.calculate_subtotal():.2f}") #shows the subtotal with 2 decimal. calling the calculate subtotal method
        return True

    def calculate_subtotal(self):
        return sum(item.price * quantity for item, quantity in self.items) #formula. return ths value


class POSSystem: #main method
    def __init__(self):
        self.store = Store() #calling the calsses
        self.cart = Cart()
    def get_current_datetime(self):
      return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def welcome_message(self): #just a message
        print("====================================")
        print("      WELCOME TO BEST BUY #418      ")
        print("     124 CONSTANT SPRING ROAD       ")
        print("         Tele:876-123-764          " )
        print("====================================")

    def main_menu(self): #main menu user promt
        while True:
            print("\nMain Menu:")
            print("1. Add Items to Cart")
            print("2. Remove Items from Cart")
            print("3. View Cart ")# option to view the cart
            print("4.checkout")# option to proceed to checkout
            print("5. Exit")# option to exit the program

            choice = input("Select an option: ")

            if choice == '1': #if statement that corresponds with the users input
                self.add_items_to_cart()
            elif choice == '2':
                self.remove_items_from_cart()
            elif choice == '3':
                self.view_cart(show_subtotal=True) # call the view_cart with show_subtotal= true
            elif choice== '4' :
                  self.checkout()
            elif choice == '5':
                print("Exiting the POS System... Thank you!")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_items_to_cart(self): 
        while True:
            self.store.display_products() #calls method catalog
            item_number = input("\nEnter the number of the item you want to add: ") #takes the users input

            if item_number not in self.store.product_catalog: #validation if the number entered is not one of the availabel options
                print("Invalid item number. Please try again.") #error message
                continue

            product = self.store.product_catalog[item_number] #assigning to product the item based on the number user enetered

            while True: #while loop to validate the quantityt of the item entered
                try:
                    quantity = int(input(f"Enter quantity for {product.item} (Stock: {product.stock}): "))

                    if quantity < 1:
                        print("Quantity must be at least 1. Please try again.")
                    elif quantity > product.stock:
                        print(f"Not enough stock! Available: {product.stock}. Please enter a lower quantity.")
                    else:
                        self.cart.add_item(product, quantity)
                        break  #exiting the quantity validation
                except ValueError:
                    print("Invalid input. Enter a valid number.")

            add_more = input("Would you like to add another item? (yes/no): ").lower() #after the user has aded an item to cart it ask if they would like to add another item 
            if add_more != 'yes':
                break  #exit the loop


    def remove_items_from_cart(self): #remove item function
        if not self.cart.view_cart(): #callign the view cart method
            return  #exiting if the cart is empty

        while True:
            try:
                item_index = int(input("Enter the number of the item you want to remove: ")) #a neumber is assigned to each item in the cart the (index)
                confirm = input("Are you sure? (1 for Yes, 2 for No): ") #comfirmation message 

                if confirm == '1':
                    self.cart.remove_item(item_index)
                    break  #exits the loop after the specified item is remeoved
                elif confirm == '2':
                    break  #exits without removing an item
                else:
                    print("Invalid input. Please enter 1 or 2.") #error message
            except ValueError: #exception handling
                print("Invalid input. Enter a valid number.")

    def view_cart(self,show_subtotal=False): #view cart method
         if self.cart.view_cart():
             if self.cart.view_cart(show_subtotal):  # Call the Cart's view_cart method
              if show_subtotal:  # Only ask to checkout if showing subtotal
                checkout_choice = input("Would you like to checkout? (1 for Yes, 2 for No): ")
                if checkout_choice == '1':
                    self.checkout()  # Call the checkout method if the user wants to proceed


    def checkout(self):
        #formulas and calculations
        subtotal = self.cart.calculate_subtotal() 
        discount = 0.05 * subtotal if subtotal > 5000 else 0
        discounted_total = subtotal - discount
        sales_tax = discounted_total * 0.10
        total_due = discounted_total + sales_tax

        print(f"\nSubtotal: ${subtotal:.2f}")
        if discount > 0:
           print(f"Sales Tax (10%): ${sales_tax:.2f}")
        print(f"Discount (5% over $5000): -${discount:.2f}")
        print(f"Total Due: ${total_due:.2f}")

        while True:
            try:
                payment_method = input("Select payment method (cash/card): ")
                amount_received = float(input("Enter payment amount: "))
                # Validate payment method
                if payment_method not in ['cash', 'card']:
                    print("Invalid payment method. Please enter 'cash' or 'card'.")
                    continue

                if amount_received < total_due:
                    print("Insufficient payment. Please enter a valid amount.") #validation
                    continue  # Continue the loop to allow re-entry of payment amount
                else:
                    change_due = amount_received - total_due
                    print(f"\nPayment of ${total_due:.2f} received{payment_method}.")
                    print(f"Change Due: ${change_due:.2f}")
                    # Capture the current date and time
                    transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.generate_receipt(subtotal, sales_tax, total_due, amount_received,payment_method, change_due,transaction_time) #calling the receipt after the payment is made
                     # Clear the cart after checkout
                    self.cart.clear_cart()  # Clear the cart
                    # View cart after checkout without showing subtotal
                    self.view_cart(show_subtotal=False)
                break
            except ValueError:
                print("Invalid input. Enter a valid amount.")
                
        
    #reciept method
    def generate_receipt(self, subtotal, sales_tax, total_due, amount_received, payment_method, change_due,transaction_time):
        
        print("====================================")
        print("             RECEIPT                ")
        print("====================================")
        print("      WELCOME TO BEST BUY #418      ")
        print("     124 CONSTANT SPRING ROAD       ")
        print("         Tele:876-123-764           ")
        print(f"Date & Time: {transaction_time}")  # Display date and time
        print("====================================")
        for item, quantity in self.cart.items:
            print(f"{item.item} x{quantity}  ${item.price:.2f}")
        print("\n")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Sales Tax: ${sales_tax:.2f}")
        print(f"Total: ${total_due:.2f}")
        print(f"Amount Paid: ${amount_received:.2f}")
        print(f"Change Due: ${change_due:.2f}")
        print("====================================")
        print("         THANK YOU!                 ")
        print("      PLEASE COME AGAIN!            ")
        print("====================================")


# Run the POS system
pos = POSSystem() #after the recepit is printed its starts over again from the beginning.
pos.welcome_message()
pos.main_menu()

