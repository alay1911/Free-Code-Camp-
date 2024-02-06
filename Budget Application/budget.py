class Category:
    """Instantiate objects based on different budget categories."""

    def __init__(self, name):
        """Initialize the category."""
        self.name = name
        self.ledger = list()
        self.funds = 0

    def __str__(self):
        """Creating an item list with all the different deposits, withdrawels and transfers."""
        # Creating title line.
        name_length = len(self.name)
        star_count = (30 - name_length) // 2
        title_line = '*'*star_count + self.name + '*'*star_count
        if len(title_line) != 30: title_line = '*' + title_line
        
        # Creating ledger list.
        ledger_list = ""
        for list_item in self.ledger:
            amt = list_item.get("amount")
            descr = list_item.get("description")
            descr = descr[:23]
            amt = '%.2f' % amt
            amt = amt[:7]
            ledger_list += descr + str(amt).rjust(30 - len(descr)) + '\n'

        # Returning full list.
        object_list = title_line + '\n' + ledger_list + 'Total: ' + str(self.funds)
        return object_list

    def deposit(self, amount, description = ""):
        """Method to deposit a certain amount with an optional description."""
        self.ledger.append({"amount": amount, "description": description})
        self.funds += amount

    def withdraw(self, amount, description = ""):
        """Method to withdraw a certain amount with an optional description."""
        if self.check_funds(amount):
            amount *= -1
            self.ledger.append({"amount": amount, "description": description})
            self.funds += amount
            return True
        else:
            return False

    def get_balance(self):
        """Method to returns current balance."""
        return self.funds

    def transfer(self, amount, budget_category):
        """Method to transfer money from one category to another."""
        if self.check_funds(amount):
            amount *= -1
            self.ledger.append({"amount": amount, "description": f"Transfer to {budget_category.name}"})
            budget_category.ledger.append({"amount": amount * -1, "description": f"Transfer from {self.name}"})
            self.funds += amount
            budget_category.funds -= amount
            return True
        else:
            return False

    def check_funds(self, amount):
        """Method to check if funds are available for certain amount."""
        if amount < self.funds:
            return True
        else:
            return False

def create_spend_chart(categories = []):
    """Function to make a bar chart showing the percentage spent in each given category."""
    # Get subtotals of each category and total.
    total = 0
    subtotals = dict()
    percentages = dict()
    for categ in categories:
        subtotal = 0
        for list_item in categ.ledger:
            amount = list_item.get("amount")
            if amount < 0:
                subtotal -= amount
            else:
                continue
        subtotals[categ] = subtotal
        total += subtotal

    # Get percentage rounded down to nearest 10 of each category.
    for key,value in subtotals.items():
        percent = (value / total) * 100
        percent = percent - (percent % 10)
        percentages[key] = percent

    # Get bar chart.
    #   - Percentages:
    bar_chart = "Percentage spent by category" + '\n'
    x = 100
    perc_list = sorted((value, key) for (key,value) in percentages.items())
    perc_list = sorted(perc_list, reverse = True)
    for number in range(11):
        bar_row = f"{x}".rjust(3) + "| "
        for value,key in perc_list:
            if value >= x:
                bar_row += "o  "
            else:
                bar_row += "   "
        bar_chart += bar_row + '\n'
        x -= 10

    #   - Horizontal line:
    dash_length = len(bar_row) - 4
    bar_chart += '    ' + '-'*dash_length + '\n' 

    #   - Category names:
    len_list = list()
    for v,k in perc_list:
        category_name = k.name
        len_list.append(len(category_name))
    y = 0
    while y <= max(len_list):
        bar_row = "     "
        for value,key in perc_list:
            cat_name = key.name
            try:    
                bar_row += cat_name[y] + '  '
            except:
                bar_row += '   '
        if y <= max(len_list) - 1:
            bar_chart += bar_row + '\n'
        else:
            bar_chart += bar_row
        y = y + 1




    return bar_chart