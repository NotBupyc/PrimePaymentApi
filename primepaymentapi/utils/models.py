from pydantic import BaseModel

class initPaymentResult(BaseModel):
    result: str
    order_id: int | None

# {
# "status":"OK",
# "result": {
# 	"status":"ACTIVE",
# 	"comsn_from_payer":75,
# 	"comsn_from_webmaster":25,
# 	"payWays":{
# 	"RUB":{
# 		"1":{"comission":"8.00", "fix_sum":"3.00", "comission_RU":"5.00", "fix_sum_RU":"2.00", "min_sum":"10.00", "max_sum":"49000.00", "comment":"Оплата картой"},
# 		"2":{"comission":"7.00", "fix_sum":"0.00", "min_sum":"10.00", "max_sum":"50000.00", "comment":""},
# 		"5":{"comission":"7.00", "fix_sum":"0.00", "min_sum":"10.00", "max_sum":"75000.00", "comment":"Кошелек QIWI"}
# 		}
# 		}
# 	}
# }




class getProjectInfoFullResult(BaseModel):
    status: str
    comsn_from_payer: int
    comsn_from_webmaster: int

class getProjectBalanceResult(BaseModel):
    balance_RUB: float
    balance_USD: float
    balance_EUR: float
    balance_UAH: float
    balance_KZT: float
    balance_CNY: float









