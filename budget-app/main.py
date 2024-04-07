class Category:
    def __init__(self, category):
        self.ledger = []
        self.category = category

    def deposit(self, amount: float, description: str=""):
        return self.ledger.append({"amount": amount, "description": description})
    

    def withdraw(self, amount: float, description: str=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(map(lambda expense: expense["amount"], self.ledger))
    
    def transfer(self, amount, to_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {to_category.category}")
            to_category.deposit(amount, f"Transfer from {self.category}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __repr__(self):
        category_length = len(self.category)
        left_padding = (30 - category_length) // 2
        right_padding = (30 - category_length - left_padding)
        display = f"{'*' * left_padding}{self.category}{'*' * right_padding}\n"
        for i, operation in enumerate(self.ledger):
            if i == 0:
                description = f"initial {operation['description'][:23]}"
            else:
                description = operation['description'][:23]
            amount = str('{:.2f}'.format(operation['amount']))[:7]
            display += f"{description}{amount.rjust(30 - len(description))}\n"
        
        display += f"Total: {self.get_balance()}\n"
        return display
    


def create_spend_chart(categories):
    pass


clothing = Category("Clothing")
clothing.deposit(1000, "deposit")
clothing.withdraw(10.15, "groceries")
clothing.withdraw(15.89, "restaurant and more food for dessert")
food = Category("Food")
clothing.transfer(50, food)
print(clothing)