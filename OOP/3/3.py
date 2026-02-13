class BankDeposit:
    def __init__(self, name, balance, rate):
        self.name = name
        self.balance = balance
        self.rate = rate

    def __calculate_profit(self):
        return (self.balance * self.rate) / 100

    def get_balance_with_profit(self):
        return self.balance + self.__calculate_profit()
