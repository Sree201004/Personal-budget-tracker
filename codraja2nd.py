import json
from datetime import datetime

class BudgetTracker:
    def __init__(self, file_name='transactions.json'):
        self.file_name = file_name
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.file_name, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transactions(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def add_transaction(self, t_type, category, amount):
        transaction = {
            'type': t_type,
            'category': category,
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expense = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        return total_income - total_expense

    def analyze_expenses(self):
        categories = {}
        for t in self.transactions:
            if t['type'] == 'expense':
                if t['category'] in categories:
                    categories[t['category']] += t['amount']
                else:
                    categories[t['category']] = t['amount']
        return categories

    def display_menu(self):
        while True:
            print("\nBudget Tracker")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. Calculate Budget")
            print("4. Analyze Expenses")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                self.add_income()
            elif choice == '2':
                self.add_expense()
            elif choice == '3':
                self.display_budget()
            elif choice == '4':
                self.display_expense_analysis()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_income(self):
        category = input("Enter income category: ")
        amount = float(input("Enter income amount: "))
        self.add_transaction('income', category, amount)
        print("Income added successfully.")

    def add_expense(self):
        category = input("Enter expense category: ")
        amount = float(input("Enter expense amount: "))
        self.add_transaction('expense', category, amount)
        print("Expense added successfully.")

    def display_budget(self):
        budget = self.calculate_budget()
        print(f"Remaining Budget: ${budget:.2f}")

    def display_expense_analysis(self):
        expenses = self.analyze_expenses()
        print("Expense Analysis:")
        for category, amount in expenses.items():
            print(f"{category}: ${amount:.2f}")

if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.display_menu()
