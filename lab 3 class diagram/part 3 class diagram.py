class Bank:
    def __init__(self):
        self.__User = []
        self.__ATMcard = []
        self.__ATMmachine = []

    def add_user(self, user):
        self.__User.append(user)
    
    def remove_user(self, user):
        self.__User.remove(user)
    
    def add_ATMcard(self, atmcard):
        self.__ATMcard.append(atmcard)
    
    def remove_ATMcard(self, atmcard):
        self.__ATMcard.remove(atmcard)
        
    def add_ATMmachine(self, atmmachine):
        self.__ATMmachine.append(atmmachine)

    def remove_ATMmachine(self, atmmachine):
        self.__ATMmachine.remove(atmmachine)
        
    def get_user(self, citizen_id: str):
        for user in self.__User:
            if user.citizen_id == citizen_id:
                return user
        return None
    
    def get_atm(self, machine_id: str):
        for atm in self.__ATMmachine:
            if atm.ATMMachine_id == machine_id:
                return atm
        return None
    
    def get_card(self, card_number: str):
        for card in self.__ATMcard:
            if card.card_number == card_number:
                return card
        return None

class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__account_num = []

    @property
    def citizen_id(self) -> str:
        return self.__citizen_id
    
    @property
    def name(self) -> str:
        return self.__name
    
    def add_account(self, account):
        self.__account_num.append(account)
    
    def find_account(self, account_number: str):
        for account in self.__account_num:
            if account.account_number == account_number:
                return account
        return None

class Account:
    def __init__(self, account_number: str, owner: User, balance: float):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = balance
        self.__transactions_history = []
    
    @property
    def account_number(self) -> str:
        return self.__account_number
    
    @property
    def owner(self) -> User:
        return self.__owner

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def transactions_history(self) -> list:
        return self.__transactions_history

    def add_transaction(self, transaction: str):
        self.__transactions_history.append(transaction)
        
    @balance.setter
    def balance(self, balance: float):
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = balance
    
    def deposit(self, amount: float):
        if amount > 0 :
            self.__balance += amount
        else:
            return "Invalid Amount!"
    
    def withdraw(self, amount: float):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
        else:
            return "Invalid Amount!"

class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin
    
    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def account(self) -> Account:
        return self.__account
    
    @property
    def owner(self) -> User:
        return self.__account.owner
    
    @property
    def balance(self) -> float:
        return self.__account.balance
    @property
    def account_number(self) -> str:
        return self.__account.account_number

    def add_transaction(self, transaction):
        self.__account.add_transaction(transaction)
    
    def validatePIN(self, input_pin) -> bool:
        if input_pin == self.__pin:
            return True
        else:
            return False

class ATMMachine:
    #annual_fee: int = 150
    #maximum_withdrawal: int = 40000
    def __init__(self, ATMMachine_id: str, atm_balance: float = 1000000):
        self.__ATMMachine_id = ATMMachine_id
        self.__atm_balance = atm_balance

    @property
    def ATMMachine_id(self) -> str:
        return self.__ATMMachine_id

    @property
    def atm_balance(self) -> float:
        return self.__atm_balance

    def insert_card(self, card_number: str, pin: str): 
        inserted_card = bank.get_card(card_number)
        if inserted_card and inserted_card.validatePIN(pin):
            return inserted_card
        return "Invalid PIN or card not found"
    
    def deposit(self, account: Account, amount: float):
        if amount > 0:
            account.deposit(amount)
            self.__atm_balance += amount
            account.add_transaction(Transaction('D', amount, account.balance, self.__ATMMachine_id))
            return "Success"
        return "Error!! the amount must be greater than 0"
    
    def withdraw(self, account: Account, amount: float):
        try:
            if amount <= 0:
                return "The withdrawal amount must be positive"
            if amount > self.__atm_balance:
                return "Insufficient funds in ATM"
            if amount > 40000: # exceeding the maximum amount per day for withdrawal
                return "Daily withdrawal limit exceeded (40,000 Baht)"
            if amount > account.balance:
                return "Insufficient funds in the account"
            account.balance -= amount
            self.__atm_balance -= amount
            account.add_transaction(Transaction('W', amount, account.balance, self.__ATMMachine_id))
            return "Success"
        except:
            return "Error occurred while withdrawing funds"
    
    def transfer(self, sender: Account, receiver: Account, amount: float):
        try:
            if amount <= 0:
                return "The transfer amount must be positive"
            if amount > sender.balance:
                return "Insufficient funds in the sender account"
            sender.balance -= amount
            receiver.balance += amount
            sender.add_transaction(Transaction('TW', amount, sender.balance, self.__ATMMachine_id, receiver.account_number))
            receiver.add_transaction(Transaction('TD', amount, receiver.balance, self.__ATMMachine_id, sender.account_number))
            return "Success"
        except:
            return "Error occurred while transferring funds"
        

class Transaction:
    def __init__(self, transaction_type: str, amount: float, balance: float, ATMMachine_id: str, account_number: str = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__balance = balance    
        self.__ATMMachine_id = ATMMachine_id
        self.__account_number = account_number
    
    def __str__(self):
        if self.__transaction_type in ('TW', 'TD'):
            return f'{self.__transaction_type}-ATM : {self.__ATMMachine_id}-{self.__amount}-{self.__balance}'
        return f'{self.__transaction_type}-ATM : {self.__ATMMachine_id}-{self.__amount}-{self.__balance}'

##################################################################################
user_data = {
    '1-1101-12345-12-0': ['Harry Potter', '1234567890', '12345', 20000],
    '1-1101-12345-13-0': ['Hermione Jean Granger', '0987654321', '12346', 1000]
    }
atm_data = {'1001': 1000000, '1002': 200000}

bank = Bank()
user = User(None, None)

for atm_id, balance in atm_data.items():
    atm_instance = ATMMachine(atm_id,balance)
    bank.add_ATMmachine(atm_instance)

for citizen_id, data in user_data.items():
    user_data = User(citizen_id, data[0])
    account_data = Account(data[1], user_data, data[3] )
    atm_card_data = ATMCard(data[2], account_data, '1234')

    bank.add_ATMcard(atm_card_data)
    bank.add_user(user_data)
    user.add_account(atm_card_data)

##################################################################################

print("--------------------------")
print("     Start Test Cases     ")
print("--------------------------")


## Test case #1: Test inserting Harry's ATM card into ATM machine #1
## and call the corresponding method.
## Expected result: Print Harry's account number and ATM card number correctly.
## Ans: 12345, 1234567890, Success
# print("-------------------------")

print("TESTCASE #1")
atm = bank.get_atm('1001')
card = atm.insert_card('12345', '1234')
print(card.card_number, card.account_number, 'Success')
print("-------------------------")

## Test case #2: Test depositing 1000 Baht into Hermione's account using ATM machine #2.
## Call the deposit method.
## Expected result: Display Hermione's balance before and after the deposit, along with the transaction.
## Hermione's account before test: 1000
## Hermione's account after test: 2000
# print("-------------------------")

print("TESTCASE #2")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(f'Hermione account balance before: {card.account.balance:,}')
atm.deposit(card.account, 1000)
print(f'Hermione account balance after: {card.account.balance:,}')
print("-------------------------")

## Test case #3: Test depositing -1 Baht into Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print("TESTCASE #3")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(atm.deposit(card.account, -1))
print("-------------------------")

## Test case #4: Test withdrawing 500 Baht from Hermione's account using ATM machine #2.
## Call the withdrawal method.
## Expected result: Display Hermione's balance before and after the withdrawal, along with the transaction.
## Hermione's account before test: 2000
## Hermione's account after test: 1500
# print("-------------------------")

print("TESTCASE #4")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(f'Hermione account balance before: {card.account.balance:,}')
atm.withdraw(card.account, 500)
print(f'Hermione account balance after: {card.account.balance:,}')
print("-------------------------")

## Test case #5: Test withdrawing 2000 Baht from Hermione's account using ATM machine #2.
## Expected result: Display "Error."
# print("-------------------------")

print("TESTCASE #5")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
print(atm.withdraw(card.account, 2000))
print("-------------------------")
## Test case #6: Test transferring 10,000 Baht from Harry's account to Hermione's account using ATM machine #2.
## Call the transfer method.
## Expected result: Display Harry's balance before and after the transfer, Hermione's balance before and after the transfer, and the transaction log.
## Harry's account before test: 20000
## Harry's account after test: 10000
## Hermione's account before test: 1500
## Hermione's account after test: 11500
# print("-------------------------")

print("TESTCASE #6")
atm = bank.get_atm('1002')
sender_card = atm.insert_card('12345', '1234') # Harry
receiver_card = atm.insert_card('12346', '1234') # Hermione
print(f"Harry's account before test: {sender_card.account.balance:,}")
print(f"Hermione's account before test: {receiver_card.account.balance:,}")
atm.transfer(sender_card.account, receiver_card.account, 10000)
print(f"Harry's account after test: {sender_card.account.balance:,}")
print(f"Hermione's account after test: {receiver_card.account.balance:,}")
print("-------------------------")

## Test case #7: Display all of Hermione's transactions.
## Expected result:
## Hermione's transaction log:
## D-ATM:1002-1000-2000
## W-ATM:1002-500-1500
## TD-ATM:1002-10000-11500
# print("-------------------------")

print("TESTCASE #7")
atm = bank.get_atm('1002')
card = atm.insert_card('12346', '1234')
for transaction in card.account.transactions_history:
    print(transaction)
print("-------------------------")



## Test case #8: Test inserting an incorrect PIN.
## Call the method to insert the card and check the PIN.
## atm_machine = bank.get_atm('1001')
## test_result = atm_machine.insert_card('12345', '9999')  # Incorrect PIN
## Expected result: Invalid PIN
# print("-------------------------")

print("TESTCASE #8")
atm_machine = bank.get_atm('1001')
test_result = atm_machine.insert_card('12345', '9999')  # Incorrect PIN
print(test_result)
print("-------------------------")

## Test case #9: Test withdrawing more than the daily limit (40,000 Baht).
## atm_machine = bank.get_atm('1001')
## account = atm_machine.insert_card('12345', '1234')  # Correct PIN
## harry_balance_before = account.get_balance()
## print(f"Harry's account before test: {harry_balance_before}")
## print("Attempting to withdraw 45,000 Baht...")
## result = atm_machine.withdraw(account, 45000)
## print(f"Expected result: Exceeds daily withdrawal limit of 40,000 Baht")
## print(f"Actual result: {result}")
## print(f"Harry's account after test: {account.get_balance()}")
# print("-------------------------")

print("TESTCASE #9")
atm_machine = bank.get_atm('1001')
account = atm_machine.insert_card('12345', '1234')  # Correct PIN
harry_balance_before = account.balance
print(f"Harry's account before test: {harry_balance_before:,}")
print("Attempting to withdraw 45,000 Baht...")
result = atm_machine.withdraw(account, 45000)
print(f"Expected result: Exceeds daily withdrawal limit of 40,000 Baht")
print(f"Actual result: {result}")
print(f"Harry's account after test: {account.balance:,}")
print("-------------------------")

## Test case #10: Test withdrawing money when the ATM has insufficient funds.
## atm_machine = bank.get_atm('1002')  # Assume machine #2 has 200,000 Baht left
## account = atm_machine.insert_card('12345', '1234')
## print("Test case #10: Test withdrawal when ATM has insufficient funds.")
## print(f"ATM machine balance before: {atm_machine.get_balance()}")
## print("Attempting to withdraw 250,000 Baht...")
## result = atm_machine.withdraw(account, 250000)
## print(f"Expected result: ATM has insufficient funds.")
## print(f"Actual result: {result}")
## print(f"ATM machine balance after: {atm_machine.get_balance()}")
# print("-------------------------")

print("TESTCASE #10")
atm_machine = bank.get_atm('1002')  # Assume machine #2 has 200,000 Baht left
account = atm_machine.insert_card('12345', '1234')
print("Test case #10: Test withdrawal when ATM has insufficient funds.")
print(f"ATM machine balance before: {atm_machine.atm_balance:,}")
print("Attempting to withdraw 250,000 Baht...")
result = atm_machine.withdraw(account, 250000)
print(f"Expected result: ATM has insufficient funds.")
print(f"Actual result: {result}")
print(f"ATM machine balance after: {atm_machine.atm_balance:,}")
print("-------------------------")

