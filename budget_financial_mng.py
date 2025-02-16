class BudgetandFinancialMng:
    def __init__(self):
        self.budgets = {}

    def update_budget(self, event, amount):
        if event.id not in self.budgets:
            self.budgets[event.id] = 0
        self.budgets[event.id] += amount
        event.budget += amount

    def get_budget(self, event):
        return self.budgets.get(event.id, 0)
    
    def set_budget(self, event, new_budget):
        self.budgets[event.id] = new_budget
        event.budget = new_budget

