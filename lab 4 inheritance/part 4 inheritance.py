class Bank:
    def __init__(self, name):
        self.__Name = name
        self.__User = []
        self.__ATMmachine = []
        self.__Seller = []
    
    @property
    def name(self) -> str:
        return self.__Name
        
    def add_user(self, user):
        self.__User.append(user)
        
    def add_ATMmachine(self, atmmachine):
        self.__ATMmachine.append(atmmachine)
    
    def add_seller(self, seller):
        self.__Seller.append(seller)
        
    def search_user_from_id(self, citizen_id: str):
        for user in self.__User:
            if user.citizen_id == citizen_id:
                return user
        return "Not Found"
    
    def search_seller(self, seller_name: str):
        for seller in self.__Seller:
            if seller.name == seller_name:
                return seller
        return "Not Found"
    
    def search_atm_machine(self, machine_id: str):
        for atm in self.__ATMmachine:
            if atm.atmmachine_id == machine_id:
                return atm
        return "Not Found"

    def search_account_from_card(self, card_number: str):
        for user in self.__User:
            for account in user.account_list:
                if account.card and account.card.card_number == card_number:
                    return account
        return "Not Found"

        
    def search_account_from_account_number(self, account_number: str):
        for user in self.__User: 
            for account in user.account_list:
                if account.account_number == account_number:
                    return account
        return "Not Found"
    
class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__account_list = []

    @property
    def citizen_id(self) -> str:
        return self.__citizen_id
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def account_list(self) -> list:
        return self.__account_list
    
    def add_account(self, account):
        self.__account_list.append(account)

    def search_account(self, account_number: str):
        for account in self.__account_list:
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
    
    def transfer(self, amount: float, receiver: 'Account') -> str:
        if amount <= 0:
            return "Invalid amount"
        if amount > self.__balance:
            return "Insufficient funds"
        self.__balance -= amount
        receiver.__balance += amount
        self.add_transaction(Transaction('TW', amount, self.__account_number, receiver.account_number, source='ACCOUNT'))
        receiver.add_transaction(Transaction('TD', amount, receiver.account_number, self.__account_number, source='ACCOUNT'))
    
    def __add__(self, amount: float):
        #Deposit money using the + operator
        if amount > 0:
            self.__balance += amount

    def __sub__(self, amount: float):
        #Withdraw money using the - operator
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            
    def __iter__(self):
        return iter(self.__transactions_history)
    
class SavingsAccount(Account):
    Interest_rate = 0.5
    Type = "Savings"
    
    def __init__(self, account_number: str, owner: User, balance: float, card = None):
        super().__init__(account_number, owner, balance, "Savings")
        self.__card = card
    
    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, card):
        self.__card = card
    
class FixDepositAccount(Account):
    Interest_rate = 2.5
    Type = "FixDeposit"
    
    def __init__(self, account_number: str, owner: User, balance: float, card = None):
        super().__init__(account_number, owner, balance, "Fixed Deposit")


class Card:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin
        
    @property
    def account(self) -> Account:
        return self.__account

    @property
    def pin(self) -> str:
        return self.__pin

    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def amount(self) -> float:
        return self.__account.amount

    @property
    def account_number(self) -> str:
        return self.__account.account_number
    
class ATMCard(Card):
    #ATMCard_fee = 150
    
    def __init__(self, card_number: str, account: Account, pin: str = '0000'):
        super().__init__(card_number, account, pin)
        self.__pin = pin
        
    def validatePIN(self, input_pin) -> bool:
        if input_pin == self.__pin:
            return True
        else:
            return False
        
class DebitCard(Card):
    #DebitCard_fee = 300
    
    def __init__(self, card_number: str, account: Account, pin: str = '0000'):
        super().__init__(card_number, account, pin)
        self.__pin = pin
        
    def validatePIN(self, input_pin) -> bool:
        if input_pin == self.__pin:
            return True
        else:
            return False
        
class ATMMachine:
    #Maximum_withdrawal: int = 20000
    def __init__(self, atmmachine_id: str, atm_balance: float = 1000000):
        self.__atmmachine_id = atmmachine_id
        self.__atm_balance = atm_balance

    @property
    def atmmachine_id(self) -> str:
        return self.__atmmachine_id

    @property
    def atm_balance(self) -> float:
        return self.__atm_balance
    
    def insert_card(self, card: Card, pin: str): 
        if card and card.validatePIN(pin):
            return "Success"
        return "Invalid PIN or card not found"
    
    def deposit(self, account: Account, amount: float):
        if amount > 0:
            account + amount
            self.__atm_balance += amount
            account.add_transaction(Transaction('D', amount, self.__atmmachine_id, source='ATM'))
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
            account - amount
            self.__atm_balance -= amount
            account.add_transaction(Transaction('W', amount, self.__atmmachine_id, source='ATM'))
            return "Success"
        except:
            return "Error occurred while withdrawing funds"
    
    def transfer(self, sender: Account, receiver: Account, amount: float):
        try:
            if amount <= 0:
                return "The transfer amount must be positive"
            if amount > sender.balance:
                return "Insufficient funds in the sender account"
            sender - amount
            receiver.balance += amount
            sender.add_transaction(Transaction('TW', amount, self.__atmmachine_id, receiver.account_number, source='ATM'))
            receiver.add_transaction(Transaction('TD', amount, self.__atmmachine_id, sender.account_number, source='ATM'))
            return "Success"
        except:
            return "Error occurred while transferring funds"
        
class Transaction:
    def __init__(self, transaction_type: str, amount: float, ATMMachine_id: str, target_account: str = None, source: str = None):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__ATMMachine_id = ATMMachine_id
        self.__target_account = target_account
        self.__source = source
        
    def __str__(self): 
        if self.__transaction_type in ('TW', 'TD', 'P', 'R'):
            return f"{self.__transaction_type}-{self.__source} : {self.__ATMMachine_id}-{self.__amount}-{self.__target_account}"
        return f"{self.__transaction_type}-{self.__source} : {self.__ATMMachine_id}-{self.__amount}"

class Seller:
    def __init__(self, seller_id: str, name: str):
        self.__seller_id = seller_id
        self.__name = name
        self.__edc_list = []

    @property
    def seller_id(self) -> str:
        return self.__seller_id

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def edc_list(self) -> list:
        return self.__edc_list
    
    def add_edc(self, edc) -> None:
        self.__edc_list.append(edc)
    
    def get_edc(self, edc_number: str):
        for edc in self.__edc_list:
            if edc.edc_id == edc_number:
                return edc
            
    def search_edc_from_number(self, edc_number: str):
        for edc in self.__edc_list:
            if edc.edc_id == edc_number:
                return edc
        return "Not found"
    
    def paid(self, card: Card, amount: float, seller_account: Account) -> str:
        if amount <= 0:
            return "Payment amount must be positive"
        if card.account.balance < amount: 
            return "Insufficient funds"
        card.account - amount  
        seller_account + amount 
        card.account.add_transaction(Transaction('P', amount, self.__seller_id, seller_account.account_number, source='COUT'))
        seller_account.add_transaction(Transaction('R', amount, self.__seller_id, card.account.account_number, source='COUT'))
        return "Payment successful"
    
class EDCmachine:
    def __init__(self,edc_id,seller):
        self.__edc_id = edc_id
        self.__seller = seller

    @property
    def edc_id(self) -> str:
        return self.__edc_id
    
    @property
    def seller(self) -> Seller:
        return self.__seller

    def paid(self, card: Card, amount: float, seller_account: Account) -> str:
        if amount <= 0:
            return "Payment amount must be positive"
        if card.account.balance < amount:
            return "Insufficient funds"
        card.account - amount
        seller_account + amount
        card.account.add_transaction(Transaction('P', amount, self.__edc_id, seller_account.account_number, source='EDC'))
        seller_account.add_transaction(Transaction('R', amount, self.__edc_id, card.account.account_number, source='EDC'))
        return "Payment successful"   
 
##################################################################################

# Define the format of the user as follows: {Citizen ID: [Name, Account Type, Account Number, Account Balance, Card Type, Card Number]}

user_data = user_data = {
    "1-1101-12345-12-0": [  # Harry Potter (Single account)
        ["Harry Potter", "Savings", "1234567890", 20000, "ATM", "12345"]
    ],
    "1-1101-12345-13-0": [  # Hermione Jean Granger (Multiple accounts)
        ["Hermione Jean Granger", "Savings", "0987654321", 2000, "Debit", "12346"],
        ["Hermione Jean Granger", "Fix Deposit", "0987654322", 1000, "", ""]  # No card for this account
    ],
    "9-0000-00000-01-0": [  # KFC (Business account, no card)
        ["KFC", "Savings", "0000000321", 0, "", ""]
    ],
    "9-0000-00000-02-0": [  # Tops (Business account, no card)
        ["Tops", "Savings", "0000000322", 0, "", ""]
    ]
}

atm_data ={'1001':1000000,'1002':200000}

seller_dic = {'210':"KFC", '220':"Tops"}

EDC = {'2101':"KFC", '2201':"Tops"}

scb = Bank('scb')

for atm_id, balance in atm_data.items():
    atm_data = ATMMachine(atm_id,balance)
    scb.add_ATMmachine(atm_data)

for seller_id, name in seller_dic.items():
    seller = Seller(seller_id, name)
    scb.add_seller(seller)
    for edc_id, edc_seller_name in EDC.items():
        if edc_seller_name == name:
            edc = EDCmachine(edc_id, seller)
            seller.add_edc(edc)

for citizen_id, data in user_data.items():
    for info in data:
        user_obj = User(citizen_id, info[0])  
        account = Account(info[2], user_obj, info[3])  
        user_obj.add_account(account)  

        if info[4] == 'ATM':
            card = ATMCard(info[5], account, '1234')
        elif info[4] == 'Debit':
            card = DebitCard(info[5], account, '1234')
        
        account.card = card  
        scb.add_user(user_obj)  
        print(f"Added user {info[0]} with account {info[2]} and card {info[4]}")



##################################################################################

print("--------------------------")
print("     Start Test Cases     ")
print("--------------------------")

# Test case #1: Test deposit from an ATM using Harry's ATM card.
# The card must be inserted first. Locate ATM machine 1 and Harry's ATM card.
# Then call the function or method `deposit` from the ATM machine and use `+` from the account.
# Expected outcome:
# Test Case #1
# Harry's ATM No :  12345
# Harry's Account No :  1234567890
# Success
# Harry account before deposit :  20000
# Deposit 1000
# Harry account after deposit :  21000

atm_machine = scb.search_atm_machine('1001')
harry_account = scb.search_account_from_card('12345')
atm_card = harry_account.card
print(atm_card.account_number)
print("Test Case #1")
print("Harry's ATM No : ",atm_card.card_number)
print("Harry's Account No : ",harry_account.account_number)
print(atm_machine.insert_card(atm_card, "1234"))
print("Harry account before deposit : ",harry_account.balance)
print("Deposit 1000")
atm_machine.deposit(harry_account,1000)
print("Harry account after deposit : ",harry_account.balance)
print("")

# Test case #2: Test withdrawal from an ATM using Hermione's ATM card.
# The card must be inserted first. Locate ATM machine 2 and Hermione's ATM card.
# Then call the function or method `withdraw` from the ATM machine and use `-` from the account.
# Expected outcome:
# Test Case #2
# Hermione's ATM No :  12346
# Hermione's Account No :  0987654321
# Success
# Hermione account before withdraw :  2000
# withdraw 1000
# Hermione account after withdraw :  1000

atm_machine = scb.search_atm_machine('1002')
hermione_account = scb.search_account_from_card('12346')
atm_card = hermione_account.card
print("Test Case #2")
print("Hermione's ATM No : ", atm_card.card_number)
print("Hermione's Account No : ", hermione_account.account_number)
print(atm_machine.insert_card(atm_card, "1234"))
print("Hermione account before withdraw : ",hermione_account.balance)
print("withdraw 1000")
atm_machine.withdraw(hermione_account,1000)
print("Hermione account after withdraw : ",hermione_account.balance)
print("")

# Test case #3: Test transferring 10,000 THB from Harry's account to Hermione's account at the counter.
# Call the method for performing the money transfer.
# Expected outcome:
# Test Case #3
# Harry's Account No :  1234567890
# Hermione's Account No :  0987654321
# Harry account before transfer :  21000
# Hermione account before transfer :  1000
# Harry account after transfer :  11000
# Hermione account after transfer :  11000

harry_account = scb.search_account_from_card('12345')
hermione_account = scb.search_account_from_card('12346')
print("Test Case #3")
print("Harry's Account No : ",harry_account.account_number)
print("Hermione's Account No : ", hermione_account.account_number)
print("Harry account before transfer : ",harry_account.balance)
print("Hermione account before transfer : ",hermione_account.balance)
harry_account.transfer(10000, hermione_account)
print("Harry account after transfer : ",harry_account.balance)
print("Hermione account after transfer : ",hermione_account.balance)
print("")

# Test case #4: Test payment using a card reader. Call the `paid` method from the card reader.
# Hermione makes a payment of 500 THB to KFC using her own card.
# Expected outcome:
# Hermione's Debit Card No :  12346
# Hermione's Account No :  0987654321
# Seller :  KFC
# KFC's Account No :  0000000321
# KFC account before paid :  0
# Hermione account before paid :  11000
# KFC account after paid :  500
# Hermione account after paid :  10500

hermione_account = scb.search_account_from_account_number('0987654321')
debit_card = hermione_account.card
kfc_account = scb.search_account_from_account_number('0000000321')
kfc = scb.search_seller('KFC')
edc = kfc.search_edc_from_number('2101')

print("Test Case #4")
print("Hermione's Debit Card No : ", debit_card.card_number)
print("Hermione's Account No : ",hermione_account.account_number)
print("Seller : ", kfc.name)
print("KFC's Account No : ", kfc_account.account_number)
print("KFC account before paid : ",kfc_account.balance)
print("Hermione account before paid : ",hermione_account.balance)
edc.paid(debit_card, 500, kfc_account)
print("KFC account after paid : ",kfc_account.balance)
print("Hermione account after paid : ",hermione_account.balance)
print("")

# Test case #5: Test electronic payment by calling the `paid` method from KFC.
# Hermione makes a payment of 500 THB to Tops.
# Expected outcome:
# Test Case #5
# Hermione's Account No :  0987654321
# Tops's Account No :  0000000322
# Tops account before paid :  0
# Hermione account before paid :  10500
# Tops account after paid :  500
# Hermione account after paid :  10000

hermione_account = scb.search_account_from_account_number('0987654321')
debit_card = hermione_account.card  
tops_account = scb.search_account_from_account_number('0000000322')
tops = scb.search_seller('Tops')
print("Test Case #5")
print("Hermione's Account No : ",hermione_account.account_number)
print("Tops's Account No : ", tops_account.account_number)
print("Tops account before paid : ",tops_account.balance)
print("Hermione account before paid : ",hermione_account.balance)
tops.paid(debit_card, 500, tops_account)  
print("Tops account after paid : ",tops_account.balance)
print("Hermione account after paid : ",hermione_account.balance)
print("")

# Test case #6: Display all transactions of Hermione using a `for` loop.
print("Test Case #6")
hermione_account = scb.search_account_from_account_number('0987654321')
print("Hermione's Account Number : ",hermione_account.account_number)
print("Transaction : ")
for transaction in hermione_account:
    print(transaction)