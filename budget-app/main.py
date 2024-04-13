class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = sum(item["amount"] for item in self.ledger)
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        for item in self.ledger:
            description = item["description"][:23]
            amount = "{:.2f}".format(item["amount"])[:7].rjust(7)
            items += f"{description}{amount.rjust(30 - len(description))}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Function to calculate the percentage spent in each category
    def get_spent_percentage(category):
        withdrawals = sum(item["amount"] for item in category.ledger if item["amount"] < 0)
        total_withdrawals = sum(
            item["amount"] for category in categories for item in category.ledger if item["amount"] < 0)
        return (withdrawals / total_withdrawals) * 100

    # Determine the maximum category name length
    max_name_length = max(len(category.category) for category in categories)

    # Generate the spend percentages for each category
    spent_percentages = [get_spent_percentage(category) for category in categories]

    # Generate the chart
    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        line = f"{i:3}| "
        for percentage in spent_percentages:
            if percentage >= i:
                line += "o  "
            else:
                line += "   "
        chart += line + "\n"

    # Generate the horizontal line below the bars
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Generate the category labels below the bars
    for i in range(max_name_length):
        line = "     "
        for category in categories:
            if i < len(category.category):
                line += category.category[i] + "  "
            else:
                line += "   "
        if i == (len(range(max_name_length)) - 1):
            chart += line + " " * ((len(categories) * 3 + 4) - len(line))
        else:
            chart += line + " " * ((len(categories) * 3 + 4) - len(line)) + "\n"

    return chart


clothing = Category("Clothing")
clothing.deposit(1000, "deposit")
clothing.withdraw(10.15, "groceries")
clothing.withdraw(15.89, "restaurant and more food for dessert")
food = Category("Food")
clothing.transfer(50, food)
print(clothing)

food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(60, "groceries")
food.withdraw(0, "restaurant and more food for dessert")

clothing = Category("Clothing")
clothing.deposit(200, "initial deposit")
clothing.withdraw(20, "pants")
clothing.withdraw(0, "shirt")

auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(10, "fuel")

categories = [food, clothing, auto]

print(create_spend_chart(categories))
