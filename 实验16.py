class bank:
    def __init__(self,bank_name):
        self.bank_name=bank_name

        @classmethod
        def get_bank_info(cls, bank_name):
            cls._name = bank_name

bank_name = 'xx银行'
        # 这是类方法     ↑
class account:
    def __init__(self,account_number,customer_name,balance):
        self.account_number=account_number
        self.customer_name=customer_name
        self.balance=balance

    def deposit(self,amount):
        if amount>0:
            self.balance=self.balance+amount
            print(f'存款成功，当前金额为:{self.balance}')
        else:
         print('存款数需大于零')
    def withdraw(self,amount):
        if 0<amount<self.balance:
            self.balance=self.balance-amount
            print(f'取款成功,剩余金额为{self.balance}')
        else:
            print('余额不足或金额出现错误')
    def get_account_info(self):
        print(f'账户号码为{self.account_number}')
        print(f'客户姓名为{self.customer_name}')
        print(f'当前余额为{self.balance}')
#这是实例方法       ↑
@staticmethod
def validate_account_number(account_number):
    if len(account_number) == 8 and account_number.isdigit():
        return True
    else:
        return False
#这是静态方法    ↑
if __name__ == "__main__":
    print(bank_name)
    try:
        acc1 = account("12345678", "张三",0.1)
        print("\n账户创建成功！")
    except ValueError as e:
        print(f"账户创建失败：{e}")
    acc1.deposit(5000)
    acc1.withdraw(2000)
    print(acc1.get_account_info())
    try:
        acc2 = account("12345", "李四",0)
    except ValueError as e:
        print(f"\n账户创建失败：{e}")

