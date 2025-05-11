# CNS_OPTIMIZED_BANKING_SYSTEM.py

class BankAccount:
    def __init__(self, acc_no: str, acc_holder: str, balance: float = 0.0):
        self.__acc_no = acc_no
        self.__acc_holder = acc_holder
        self.__balance = balance

    def deposit(self, amount: float, note: str = None):
        self.__balance += amount
        msg = f"Deposited {amount} to Account: {self.__acc_no}"
        if note: msg += f" - Note: {note}"
        print(msg)

    def withdraw(self, amount: float):
        if amount > self.__balance:
            print("Insufficient Funds")
            return False
        self.__balance -= amount
        print(f"Withdrew {amount} from Account: {self.__acc_no}. New Balance: {self.__balance}")
        return True

    def get_balance(self):
        return self.__balance

    def get_details(self):
        return (self.__acc_no, self.__acc_holder, self.__balance)

    def transfer(self, target_acc, amount: float):
        if self.withdraw(amount):
            target_acc.deposit(amount)
            print(f"Transferred {amount} from {self.__acc_no} to {target_acc.__acc_no}")

class SavingsAccount(BankAccount):
    def __init__(self, acc_no: str, acc_holder: str, balance: float = 0.0, interest_rate: float = 0.04):
        super().__init__(acc_no, acc_holder, balance)
        self.__interest_rate = interest_rate

    def apply_interest(self):
        interest = self.get_balance() * self.__interest_rate
        self.deposit(interest, "Interest Applied")

class CheckingAccount(BankAccount):
    def __init__(self, acc_no: str, acc_holder: str, balance: float = 0.0, overdraft_limit: float = 100.0):
        super().__init__(acc_no, acc_holder, balance)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        if amount > (self.get_balance() + self.__overdraft_limit):
            print("Overdraft Limit Exceeded")
            return False
        return super().withdraw(amount)

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, acc_type: str, acc_no: str, acc_holder: str, initial_balance: float = 0.0, **kwargs):
        if acc_no in self.accounts:
            print("Account already exists!")
            return

        if acc_type.lower() == "savings":
            self.accounts[acc_no] = SavingsAccount(acc_no, acc_holder, initial_balance, **kwargs)
        elif acc_type.lower() == "checking":
            self.accounts[acc_no] = CheckingAccount(acc_no, acc_holder, initial_balance, **kwargs)
        else:
            self.accounts[acc_no] = BankAccount(acc_no, acc_holder, initial_balance)
        
        print(f"Account {acc_no} created successfully!")

    def get_account(self, acc_no: str):
        return self.accounts.get(acc_no, None)

    def transfer_funds(self, from_acc: str, to_acc: str, amount: float):
        source = self.get_account(from_acc)
        target = self.get_account(to_acc)
        if not source or not target:
            print("Invalid account(s)")
            return
        source.transfer(target, amount)

# User Interface
bank = Bank()

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer Funds")
    print("5. Check Balance")
    print("6. Apply Interest (Savings)")
    print("7. Exit")

    choice = input("Select an option: ").strip()

    if choice == "1":
        acc_type = input("Account Type (Savings/Checking/Default): ").strip()
        acc_no = input("Account Number: ").strip()
        acc_holder = input("Account Holder Name: ").strip()
        initial_balance = float(input("Initial Balance (default 0): ") or 0)
        
        if acc_type.lower() in ["savings", "checking"]:
            param = float(input(f"Enter {'Interest Rate' if 'savings' in acc_type.lower() else 'Overdraft Limit'}: "))
            bank.create_account(acc_type, acc_no, acc_holder, initial_balance, **{ 
                'interest_rate' if 'savings' in acc_type.lower() else 'overdraft_limit': param 
            })
        else:
            bank.create_account("default", acc_no, acc_holder, initial_balance)

    elif choice == "2":
        acc_no = input("Account Number: ").strip()
        amount = float(input("Deposit Amount: "))
        account = bank.get_account(acc_no)
        if account:
            account.deposit(amount)
        else:
            print("Account not found!")

    elif choice == "3":
        acc_no = input("Account Number: ").strip()
        amount = float(input("Withdrawal Amount: "))
        account = bank.get_account(acc_no)
        if account:
            account.withdraw(amount)
        else:
            print("Account not found!")

    elif choice == "4":
        from_acc = input("From Account: ").strip()
        to_acc = input("To Account: ").strip()
        amount = float(input("Transfer Amount: "))
        bank.transfer_funds(from_acc, to_acc, amount)

    elif choice == "5":
        acc_no = input("Account Number: ").strip()
        account = bank.get_account(acc_no)
        if account:
            print(f"Balance: {account.get_balance()}")
        else:
            print("Account not found!")

    elif choice == "6":
        acc_no = input("Savings Account Number: ").strip()
        account = bank.get_account(acc_no)
        if isinstance(account, SavingsAccount):
            account.apply_interest()
        else:
            print("Not a savings account or invalid account!")

    elif choice == "7":
        break

    else:
        print("Invalid choice!")