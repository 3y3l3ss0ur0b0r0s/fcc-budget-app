import math

class Category:
  name = ""
  funds = 0.00
  ledger = []

  # Constructor
  def __init__(self, name):
    #print("Constructing a Category called:", name)
    self.name = name
    self.funds = 0.00
    self.ledger = list()

  # A check_funds method that accepts an amount as an argument. It returns False if the amount is greater than the balance of the budget category and returns True otherwise. This method should be used by both the withdraw method and transfer method.
  def check_funds(self, amount):
    #print("In check_funds():")
    if amount <= self.funds:
      return True
    return False

  # A deposit method that accepts an amount and description. If no description is given, it should default to an empty string. The method should append an object to the ledger list in the form of {"amount": amount, "description": description}.
  def deposit(self, amount, description=''):
    #print("In deposit(): amount:", amount, ", description:", description)
    amount = round(amount, 2)
    #print("Appending new deposit to ledger: amount:", amount, "description:", description)
    self.funds += amount
    #print("Funds updated:", self.funds)
    self.ledger.append({"amount": amount, "description": description})

  # A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger as a negative number. If there are not enough funds, nothing should be added to the ledger. This method should return True if the withdrawal took place, and False otherwise.
  def withdraw(self, amount, description=''):
    #print("In withdraw(): amount:", amount, ", description:", description)
    amount = round(amount, 2)
    if self.check_funds(amount) == True:
      convertedAmount = amount * -1
      #print("Appending new withdrawal to ledger: convertedAmount:", convertedAmount, "description:", description)
      self.funds -= amount
      #print("Funds updated:", self.funds)
      self.ledger.append({"amount": convertedAmount, "description": description})
      return True
    return False

  # A transfer method that accepts an amount and another budget category as arguments. The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to either ledgers. This method should return True if the transfer took place, and False otherwise.
  def transfer(self, amount, category):
    #print("In transfer():")
    amount = round(amount, 2)
    if self.check_funds(amount) == True:
      #print("There are enough funds for the transfer.")
      wDescription = "Transfer to " + category.name
      self.withdraw(amount, wDescription)
      dDescription = "Transfer from " + self.name
      category.deposit(amount, dDescription)
      return True
    return False

  # A get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred.
  def get_balance(self):
    #print("In get_balance(); returning:", self.funds)
    return self.funds

  # Returns positive amount of all withdrawals in ledger
  def get_withdrawal_total(self):
    withdrawals = 0
    for item in self.ledger:
      if item["amount"] < 0:
        withdrawals += item["amount"]
    return withdrawals * -1

  # For title ("name") formatting
  def get_title_string(self):
    #print("In get_title_string():")
    numAsterisks = 30 - len(self.name)
    title_string = "*"*(int(numAsterisks/2)) + self.name + "*"*(int(numAsterisks/2))
    #print("Resulting title string:", title_string)
    return title_string

  # Get ledger as string
  def get_ledger_string(self):
    #print("In get_ledger_string():")
    ledger_string = ""
    for item in self.ledger:
      ledger_string += item["description"][:23]
      formattedAmount = format(item["amount"], ".2f")
      numSpaces = (30 - len(item["description"][:23])) - len(formattedAmount)
      ledger_string += " "*numSpaces + formattedAmount + "\n"
    ledger_string += "Total: " + str(self.get_balance())
    #print("ledger_string:", ledger_string)
    return ledger_string

  def __str__(self):
    return self.get_title_string() + "\n" + self.get_ledger_string()

# Get dict percentages of categories
def get_percentages(categories):
  category_percentage = dict()
  totalSpent = 0

  # Get amount spent in category
  for category in categories:
    totalSpent += category.get_withdrawal_total()
    #print(category.name)

  # Populate dict with percentages
  for category in categories:
    percentage = math.floor((category.get_withdrawal_total() / totalSpent) * 100)
    #print("category:", category.name, ", percentage:", percentage, ", non-rounded:", ((category.get_withdrawal_total() / totalSpent) * 100))
    category_percentage[category.name] = percentage
    
  #print(category_percentage)
  return category_percentage

# Draw bar_chart
def create_spend_chart(categories):
  #print("In create_spend_chart(categories):")
  
  # Title
  bar_chart = "Percentage spent by category"

  # Percentages
  category_percentages = get_percentages(categories)
  
  # y-axis
  i = 100
  while i >= 0:
    spaces = 3 - len(str(i))
    bar_chart += "\n" + " "*spaces + str(i) + "| "
    # Print 'o' for categories
    for key in category_percentages:
      if i <= category_percentages[key]:
        bar_chart += "o  "
      else:
        bar_chart += "   "
    i -= 10

  # x-axis
  bar_chart += '\n    -' + '---'*len(categories)

  # Category names
  categoryNames = map(lambda c: len(c.name), categories)
  maxLength = max(categoryNames)
  categoryLines = [""]*maxLength
  for i in range(maxLength):
    #print(i)
    for category in categories:
      if i < len(category.name):
        categoryLines[i] += category.name[i] + "  "
      else:
        categoryLines[i] += "   "
    bar_chart += "\n     " + categoryLines[i]

  #print(bar_chart)
  return bar_chart