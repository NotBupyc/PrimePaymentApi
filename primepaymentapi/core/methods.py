from abc import ABCMeta
from primepaymentapi.enums import PayWay

class PaymentMethod(metaclass=ABCMeta):
    def __init__(
            self,
            secret1: str | None = None,
            project_id: int | None = None,
            ) -> None:
        self.secret1 = secret1
        self.action = self.__class__.__name__
        self.project = project_id

    @property
    def to_dict(self) -> dict:
        return {
            atr: getattr(self, atr)
            for atr in list((self.__dict__.keys()))
        }

class initPayment(PaymentMethod):
    """
    Вебмастер подписывает данные подписью и делает запрос на API.
    В случае успеха в ответе будет содержаться ссылка на форму оплаты, куда вам нужно отправить пользователя.
    """
    #md5 ( secret1 + action + project + sum + currency + innerID + email + payWay )
    def __init__(
            self,
            secret1: str,
            project_id: int,

            sum: int = 100,
            currency: str = "RUB",
            innerID: int = 1,
            email: str = "user@site.com",
            payWay: PayWay = PayWay.CARDS,
            ) -> None:
        super().__init__(secret1, project_id)

        self.sum = sum
        self.currency = currency
        self.innerID = innerID
        self.email = email
        self.payWay = payWay.value


class getOrderInfo(PaymentMethod):
    """
    Получить статус оплаты по ID. Для выполнения запроса необходимо указывать ID проекта и
    подписывать запрос секретным словом 1 из этого проекта.
    """
    #md5 ( secret1 + action + project + orderID )
    def __init__(
            self,
            secret1: str,
            project_id: int,

            orderID: int
    ) -> None:
        super().__init__(secret1, project_id)
        self.project = project_id

        self.orderID = orderID

class refund(PaymentMethod):
    """
    Вернуть пользователю оплату. Метод refund можно применить к заказу, оплаченому через банк. карту.
    Баланс на вашем проекте должен быть больше чем сумма в заказе.
    """
    def __init__(
            self,
            secret1: str,
            orderID: int,
    ) -> None:
        super().__init__(secret1)

        self.orderID = orderID

class initPayout(PaymentMethod):
    # payout_key + action + project
    """
    Вебмастер подписывает данные подписью и делает запрос на API.
    Создается заявка на выплату в указаном проекте.
    """
    def __init__(
            self,
            payout_key: str,
            project_id: int,

            sum: int = 100,
            currency: str = "RUB",
            innerID: int = 1,
            payWay: PayWay = PayWay.CARDS,
            email: str = "user@site.com",
            purse: int = 1000_0000_0000_0000
    ) -> None:
        self.payout_key = payout_key

        super().__init__(project_id=project_id)

        self.sum = sum
        self.currency = currency
        self.innerID = innerID
        self.payWay = payWay
        self.email = email
        self.purse = purse

class getProjectBalance(PaymentMethod):
    pass

class getPayoutInfo(PaymentMethod):
    # md5 ( secret1 + action + project + payoutID )
    def __init__(
            self,
            secret1: str,
            project_id: int,

            payoutID: int
    ) -> None:
        super().__init__(secret1, project_id)

        self.payoutID = payoutID

class getProjectInfo(PaymentMethod):
    #md5 ( secret1 + action + project )
        pass

class getExchangeRate(PaymentMethod):
        pass



        

