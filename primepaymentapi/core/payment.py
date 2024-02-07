import json

import aiohttp
import requests
from requests import Response
import hashlib

from primepaymentapi.core.methods import (
    PaymentMethod,
    initPayment,
    getOrderInfo,
    refund,
    initPayout,
    getProjectBalance,
    getProjectInfo, getPayoutInfo
)
from primepaymentapi.enums import PayWay
from primepaymentapi.utils.models import initPaymentResult, getProjectBalanceResult


class BasePrimaryPayment:
    def __init__(
        self,
        project_id: int,
        secret_word: str,
    ) -> None:
        self.project_id = project_id
        self.secret_word = secret_word

        self.BASE_URL = 'https://pay.primepayments.io/API/v2/'

    @staticmethod
    def _get_sign(data: dict) -> str:
        data_string = "".join(list(map(str, data.values())))
        sign = hashlib.md5(data_string.encode('utf-8')).hexdigest()
        return sign

class PrimePayment(BasePrimaryPayment):

    def __call__(self, method: PaymentMethod) -> dict:
        if not isinstance(method, PaymentMethod):
            raise TypeError('method must be PaymentMethod')

        data = method.to_dict
        data['sign'] = self._get_sign(data)

        response = requests.post(self.BASE_URL, data=data)
        return response.json()

    def create_payment(
            self,
            sum: int = 100,
            currency: str = "RUB",
            innerID: int = 1,
            payWay: PayWay = PayWay.CARDS,
            email: str = "user@site.com",
    ) -> initPaymentResult:
        data = self(
            initPayment(
                secret1=self.secret_word,
                project_id=self.project_id,

                sum=sum,
                currency=currency,
                innerID=innerID,
                payWay=payWay,
                email=email,
            )
        )
        return initPaymentResult(**data)

    def get_order_info(self, orderID: int) -> dict:
        return self(
            getOrderInfo(
                secret1=self.secret_word,
                project_id=self.project_id,
                orderID=orderID
            )
        )

    def refund(self, orderID: int) -> dict:
        return self(
            refund(
                secret1=self.secret_word,
                orderID=orderID
            )
        )

    def init_payout(
            self,
            payout_key: str,
            sum: int = 100,
            currency: str = "RUB",
            payWay: PayWay = PayWay.CARDS,
            email: str = "user@site.com",
            purse: int = 1000_0000_0000_0000
    ) -> dict:
        # project, sum, currency, payWay, email, purse
        return self(
            initPayout(
                project_id=self.project_id,

                payout_key=payout_key,
                sum=sum,
                currency=currency,
                payWay=payWay,
                email=email,
                purse=purse,
            )
        )

    def get_project_balance(self) -> getProjectBalanceResult:
        data = self(
            getProjectBalance(
                secret1=self.secret_word,
                project_id=self.project_id
            )
        )
        return getProjectBalanceResult(**data['result'])

    def get_payout_info(
            self,
            payoutID: int
    ) -> dict:
        return self(
            getPayoutInfo(
                secret1=self.secret_word,
                project_id=self.project_id,
                payoutID=payoutID
            )
        )

    def get_project_info(self) -> dict:
        return self(
            getProjectInfo(
                secret1=self.secret_word,
                project_id=self.project_id
            )
        )


class AIOPrimaryPayment(BasePrimaryPayment):
    async def __call__(self, method: PaymentMethod) -> dict:
        if not isinstance(method, PaymentMethod):
            raise TypeError('method must be PaymentMethod')

        data = method.to_dict
        data['sign'] = self._get_sign(data)

        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, data=data) as response:
                content_type = response.headers.get('content-type', '').lower()
                if 'application/json' in content_type:
                    data = await response.json()

                else:
                    text = await response.text()
                    data = json.loads(text)
                    print(data)

                return data

    async def create_payment(
            self,
            sum: int = 100,
            currency: str = "RUB",
            innerID: int = 1,
            payWay: PayWay = PayWay.CARDS,
            email: str = "user@site.com",
        ) -> initPaymentResult:
        data = await self(
            initPayment(
                secret1=self.secret_word,
                project_id=self.project_id,

                sum=sum,
                currency=currency,
                innerID=innerID,
                payWay=payWay,
                email=email,
            )
        )
        return initPaymentResult(**data)

    async def get_order_info(self, orderID: int) -> dict:
        return await self(
            getOrderInfo(
                secret1=self.secret_word,
                project_id=self.project_id,
                orderID=orderID
            )
        )

    async def refund(self, orderID: int) -> dict:
        return await self(
            refund(
                secret1=self.secret_word,
                orderID=orderID
            )
        )

    async def init_payout(
            self,
            payout_key: str,
            sum: int = 100,
            currency: str = "RUB",
            payWay: PayWay = PayWay.CARDS,
            email: str = "user@site.com",
            purse: int = 1000_0000_0000_0000
    ) -> dict:
        #project, sum, currency, payWay, email, purse
        return await self(
            initPayout(
                project_id=self.project_id,

                payout_key=payout_key,
                sum=sum,
                currency=currency,
                payWay=payWay,
                email=email,
                purse=purse,
            )
        )

    async def get_project_balance(self) -> getProjectBalanceResult:
        data = await self(
            getProjectBalance(
                secret1=self.secret_word,
                project_id=self.project_id
            )
        )

        return getProjectBalanceResult(**data['result'])

    async def get_payout_info(
            self,
            payoutID: int
    ) -> dict:
        return await self(
            getPayoutInfo(
                secret1=self.secret_word,
                project_id=self.project_id,
                payoutID=payoutID
            )
        )

    async def get_project_info(self) -> dict:
        return await self(
            getProjectInfo(
                secret1=self.secret_word,
                project_id=self.project_id
            )
        )







