from primepaymentapi import PrimePayment, AIOPrimaryPayment

# Тетсовые данные
project = 1
secret = "test_API"

#print(a.create_payment())
a = PrimePayment(project, secret)

t = a.get_project_balance()
print(t.balance_RUB)
